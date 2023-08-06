import os
import pickle
from datetime import datetime

import numpy as np
import pandas as pd
import torch
from .utils import Mode, download_detection
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import Dataset

# from data.precipitation.preprocess import preprocess
# from data.utils import Mode

RAW_DATA_FILE = 'full-dataset/shifts_precipitation.csv'
ID_HELD_OUT = 0.1


class Config():
    '''
    Define Configuration for partioning data
    '''

    def __init__(self, seed=1):
        '''
        time_splits: fractions associated with TRAIN, GAP, DEV_OUT, EVAL_OUT (split on time)
        climate_splits: number of climates kept for TRAIN, DEV_OUT, EVAL_OUT (from above time splits)
        in_domain_splits: Separation TRAIN time and specified climate segment block into TRAIN, DEV_IN, EVAL_IN
        eval_dev_overlap: Flag if TRUE, EVAL_OUT climates kept include the DEV_OUT climates kept.
        '''
        self.seed = seed


class Partitioner():
    '''
    Requires a block of data and partitions it into
    the following disjoint subsets:
    1) train.csv:
                    Data for training.

    2) dev_in.csv:
                    Development data from the same domain
                    in time and climate as of the train.csv
                    data.
    3) eval_in.csv:
                    Evaluation data from the same domain
                    in time and climate as of the train.csv
                    data.
    4) dev_out.csv:
                    Data distributionally shifted in time and climate
                    from train.csv.
    5) eval_out.csv:
                    Data further distributionally shifted in climate
                    and different time frame from train.csv and dev_out.csv.
                    Can be configured to have overlap in climates
                    with dev_out.csv.
    If no_meta == True, a further set of files will be generated:
    6) dev_in_no_meta.csv:
                    Same as dev_in.csv with meta data (first 6 features)
                    removed.
    7) eval_in_no_meta.csv:
                    Same as eval_in.csv with meta data (first 6 features)
                    removed.
    8) dev_out_no_meta.csv:
                    Same as dev_out.csv with meta data (first 6 features)
                    removed.

    9) eval_out_no_meta.csv:
                    Same as eval_out.csv with meta data (first 6 features)
                    removed.
    '''

    def __init__(self, data_path, config=Config()):
        '''
        unique labels in raw data for precipitation class [ 0. 10. 11. 12. 13. 20. 21. 22. 23.]
        rewrite as [0 1 2 3 4 5 6 7 8 9]
        '''
        self.config = config
        # Read in the raw data
        chunksize = 10 ** 6
        chunks = []
        num_chunks = 0
        reader = pd.read_csv(data_path, chunksize=chunksize)
        for chunk in reader:
            print(f'chunk {num_chunks} read')
            chunks.append(chunk)
            num_chunks += 1

        self.df = pd.concat(chunks)
        # Partition the data by time segments
        self.dfs_to_save = {}
        self._split_by_time()
        # Add dummy samples for unrepresented classifcation classes
        for taskid in self.dfs_to_save.keys():
            self.dfs_to_save[taskid] = self._add_dummy(self.dfs_to_save[taskid])

    def _split_by_time(self):
        """
        Partition the data into the main time segments.
        """
        # Sort all data in time order
        self.df = self.df.sort_values(by=['fact_time'])
        print('total rows', self.df.shape[0])

        # Convert timestamp to date
        self.df.fact_time = self.df.fact_time.apply(lambda x: datetime.fromtimestamp(x))
        df_months = self.df.groupby(pd.Grouper(key='fact_time', freq='M'))
        self.dfs = [group for _, group in df_months]
        del df_months

    def _add_dummy(self, df_to_modify):
        '''
        Add dummy data for missing precipitation classes in df.
        '''
        # Identify list of all classification classes
        classes_to_check = set(list(self.df['fact_cwsm_class']))
        # Find the average of all data rows
        avg_row = df_to_modify.mean(axis=0)
        # Append averaged row for each classification class not present in the data
        for precip_class in classes_to_check:
            if precip_class not in df_to_modify['fact_cwsm_class']:
                print("Dummy added to training", precip_class)
                ind = len(df_to_modify)
                df_to_modify.loc[ind] = avg_row
                df_to_modify.at[ind, 'fact_cwsm_class'] = precip_class
        return df_to_modify

    def save(self, save_path):
        """
        Save all relevant data split files.
        """

        # Save all files
        precipitation_classes = {0.: 0, 10.: 1, 11.: 2, 12.: 3, 13.: 4, 20.: 5, 21.: 6, 22.: 7, 23.: 8}
        precipitation_dataset = {}
        for taskid in self.dfs_to_save.keys():
            # Skip month 0 which has few data points
            if taskid == 0:
                continue
            data = self.dfs_to_save[taskid].iloc[:, 3:]  # first 3 columns are meta dat
            categorical_data = data['wrf_available']
            continuous_data = data.iloc[:, data.columns != 'wrf_available']
            precipitation_labels = self.dfs_to_save[taskid]['fact_cwsm_class'].apply(lambda x: precipitation_classes[x])
            temperatures = self.dfs_to_save[taskid]['fact_temperature']

            num_samples = len(precipitation_labels)
            num_train_images = int((1 - ID_HELD_OUT) * num_samples)
            seed_ = np.random.get_state()
            np.random.seed(0)
            idxs = np.random.permutation(np.arange(num_samples))
            np.random.set_state(seed_)
            train_idxs = idxs[:num_train_images].astype(int)
            test_idxs = idxs[num_train_images + 1:].astype(int)

            precipitation_dataset[taskid] = {}
            precipitation_dataset[taskid][Mode.TRAIN] = {}
            precipitation_dataset[taskid][Mode.TRAIN]['data'] = {}
            precipitation_dataset[taskid][Mode.TRAIN]['data']['categorical'] = np.array(categorical_data.to_numpy())[
                train_idxs]
            precipitation_dataset[taskid][Mode.TRAIN]['data']['continuous'] = np.array(continuous_data.to_numpy())[train_idxs]
            precipitation_dataset[taskid][Mode.TRAIN]['labels'] = np.array(precipitation_labels.to_numpy())[train_idxs]
            precipitation_dataset[taskid][Mode.TRAIN]['temperatures'] = np.array(temperatures.to_numpy())[train_idxs]
            precipitation_dataset[taskid][Mode.TEST_ID] = {}
            precipitation_dataset[taskid][Mode.TEST_ID]['data'] = {}
            precipitation_dataset[taskid][Mode.TEST_ID]['data']['categorical'] = np.array(categorical_data.to_numpy())[
                test_idxs]
            precipitation_dataset[taskid][Mode.TEST_ID]['data']['continuous'] = np.array(continuous_data.to_numpy())[
                test_idxs]
            precipitation_dataset[taskid][Mode.TEST_ID]['labels'] = np.array(precipitation_labels.to_numpy())[test_idxs]
            precipitation_dataset[taskid][Mode.TEST_ID]['temperatures'] = np.array(temperatures.to_numpy())[test_idxs]
            precipitation_dataset[taskid][Mode.TEST_OOD] = {}
            precipitation_dataset[taskid][Mode.TEST_OOD]['data'] = {}
            precipitation_dataset[taskid][Mode.TEST_OOD]['data']['categorical'] = np.array(categorical_data.to_numpy())
            precipitation_dataset[taskid][Mode.TEST_OOD]['data']['continuous'] = np.array(continuous_data.to_numpy())
            precipitation_dataset[taskid][Mode.TEST_OOD]['labels'] = precipitation_labels.to_numpy()
            precipitation_dataset[taskid][Mode.TEST_OOD]['temperatures'] = temperatures.to_numpy()

        with open(save_path, 'wb') as f:
            pickle.dump(precipitation_dataset, f)


def preprocess_reduced_train_set(args):
    print(f'Preprocessing reduced train proportion dataset and saving to precipitation_{args.reduced_train_prop}.pkl')
    np.random.seed(0)

    orig_data_file = os.path.join(args.data_dir, f'precipitation.pkl')
    dataset = pickle.load(open(orig_data_file, 'rb'))
    num_tasks = 12
    months = [month for month in range(1, num_tasks + 1)]
    train_fraction = args.reduced_train_prop / (1 - ID_HELD_OUT)

    for month in months:
        train_categorical = dataset[month][Mode.TRAIN]['data']['categorical']
        train_continuous = dataset[month][Mode.TRAIN]['data']['continuous']
        train_labels = dataset[month][Mode.TRAIN]['labels']
        train_temperatures = dataset[month][Mode.TRAIN]['temperatures']

        num_train_samples = len(train_labels)
        reduced_num_train_samples = int(train_fraction * num_train_samples)
        idxs = np.random.permutation(np.arange(num_train_samples))
        train_idxs = idxs[:reduced_num_train_samples].astype(int)

        new_train_categorical = np.array(train_categorical)[train_idxs]
        new_train_continuous = np.array(train_continuous)[train_idxs]
        new_train_labels = np.array(train_labels)[train_idxs]
        new_train_temperatures = np.array(train_temperatures)[train_idxs]
        dataset[month][Mode.TRAIN]['data']['categorical'] = np.stack(new_train_categorical, axis=0)
        dataset[month][Mode.TRAIN]['data']['continuous'] = np.array(new_train_continuous)
        dataset[month][Mode.TRAIN]['labels'] = np.stack(new_train_labels, axis=0)
        dataset[month][Mode.TRAIN]['temperatures'] = np.array(new_train_temperatures)

    preprocessed_data_file = os.path.join(args.data_dir, f'precipitation_{args.reduced_train_prop}.pkl')
    pickle.dump(dataset, open(preprocessed_data_file, 'wb'))
    np.random.seed(args.random_seed)


def preprocess_orig(args):
    '''Partitions tabular precipitation data for distributional shift'''

    # Load the configurable parameters
    config = Config()
    print(config)

    # Partition the raw precipitation data
    data_path = os.path.join(args.data_dir, RAW_DATA_FILE)
    partitioner = Partitioner(data_path, config)

    # Print number of data points in each data split
    for name, df in partitioner.dfs_to_save.items():
        print(name, df.shape[0])

    # Save all files
    preprocessed_data_path = os.path.join(args.data_dir, 'precipitation.pkl')
    partitioner.save(preprocessed_data_path)


def preprocess(args):
    np.random.seed(0)
    if not os.path.isfile(os.path.join(args.data_dir, 'precipitation.pkl')):
        preprocess_orig(args)
    if args.reduced_train_prop is not None:
        if not os.path.isfile(os.path.join(args.data_dir, f'precipitation_{args.reduced_train_prop}.pkl')):
            preprocess_reduced_train_set(args)
    np.random.seed(args.random_seed)


continuous_cols = [
    "climate_pressure", "climate_temperature", "cmc_0_0_0_1000", "cmc_0_0_0_2", "cmc_0_0_0_2_grad",
    "cmc_0_0_0_2_interpolated", "cmc_0_0_0_2_next", "cmc_0_0_0_500", "cmc_0_0_0_700", "cmc_0_0_0_850",
    "cmc_0_0_0_925", "cmc_0_0_6_2", "cmc_0_0_7_1000", "cmc_0_0_7_2", "cmc_0_0_7_500", "cmc_0_0_7_700",
    "cmc_0_0_7_850", "cmc_0_0_7_925", "cmc_0_1_0_0", "cmc_0_1_11_0", "cmc_0_1_65_0", "cmc_0_1_65_0_grad",
    "cmc_0_1_65_0_next", "cmc_0_1_66_0", "cmc_0_1_66_0_grad", "cmc_0_1_66_0_next", "cmc_0_1_67_0",
    "cmc_0_1_67_0_grad", "cmc_0_1_67_0_next", "cmc_0_1_68_0", "cmc_0_1_68_0_grad", "cmc_0_1_68_0_next",
    "cmc_0_1_7_0", "cmc_0_2_2_10", "cmc_0_2_2_1000", "cmc_0_2_2_500", "cmc_0_2_2_700", "cmc_0_2_2_850",
    "cmc_0_2_2_925", "cmc_0_2_3_10", "cmc_0_2_3_1000", "cmc_0_2_3_500", "cmc_0_2_3_700", "cmc_0_2_3_850",
    "cmc_0_2_3_925", "cmc_0_3_0_0", "cmc_0_3_0_0_next", "cmc_0_3_1_0", "cmc_0_3_5_1000", "cmc_0_3_5_500",
    "cmc_0_3_5_700", "cmc_0_3_5_850", "cmc_0_3_5_925", "cmc_0_6_1_0", "cmc_available", "cmc_horizon_h",
    "cmc_precipitations", "cmc_timedelta_s", "gfs_2m_dewpoint", "gfs_2m_dewpoint_grad", "gfs_2m_dewpoint_next",
    "gfs_a_vorticity", "gfs_available", "gfs_cloudness", "gfs_clouds_sea", "gfs_horizon_h", "gfs_humidity",
    "gfs_precipitable_water", "gfs_precipitations", "gfs_pressure", "gfs_r_velocity", "gfs_soil_temperature",
    "gfs_soil_temperature_available", "gfs_temperature_10000", "gfs_temperature_15000", "gfs_temperature_20000",
    "gfs_temperature_25000", "gfs_temperature_30000", "gfs_temperature_35000", "gfs_temperature_40000",
    "gfs_temperature_45000", "gfs_temperature_5000", "gfs_temperature_50000", "gfs_temperature_55000", "gfs_temperature_60000",
    "gfs_temperature_65000", "gfs_temperature_7000", "gfs_temperature_70000", "gfs_temperature_75000", "gfs_temperature_80000",
    "gfs_temperature_85000", "gfs_temperature_90000", "gfs_temperature_92500", "gfs_temperature_95000", "gfs_temperature_97500",
    "gfs_temperature_sea", "gfs_temperature_sea_grad", "gfs_temperature_sea_interpolated", "gfs_temperature_sea_next",
    "gfs_timedelta_s", "gfs_total_clouds_cover_high", "gfs_total_clouds_cover_low", "gfs_total_clouds_cover_low_grad",
    "gfs_total_clouds_cover_low_next", "gfs_total_clouds_cover_middle", "gfs_u_wind", "gfs_v_wind", "gfs_wind_speed",
    "sun_elevation", "topography_bathymetry", "wrf_graupel", "wrf_hail", "wrf_psfc", "wrf_rain", "wrf_rh2", "wrf_snow",
    "wrf_t2", "wrf_t2_grad", "wrf_t2_interpolated", "wrf_t2_next", "wrf_wind_u", "wrf_wind_v"
]

categorical_cols = [
    "wrf_available"
]

def min_max_func(x, arr):
    max_val = np.max(arr)
    min_val = np.min(arr)
    new_val = (x - min_val) / (max_val - min_val)
    return new_val

def rev_min_max_func(x, arr):
    max_val = np.max(arr)
    min_val = np.min(arr)
    og_val = (x *(max_val - min_val)) + min_val
    return og_val

class PrecipitationBase(Dataset):
    def __init__(self, args):
        super().__init__()

        if args.reduced_train_prop is None:
            self.data_file = f'{str(self)}.pkl'
        else:
            self.data_file = f'{str(self)}_{args.reduced_train_prop}.pkl'

        download_detection(args.data_dir, self.data_file)
        preprocess(args)

        self.datasets = pickle.load(open(os.path.join(args.data_dir, self.data_file), 'rb'))

        self.args = args
        self.num_classes = 9
        self.current_time = 0
        self.num_tasks = 12
        self.ENV = [month for month in range(1, self.num_tasks + 1)]
        self.mini_batch_size = args.mini_batch_size
        self.regression = True if self.args.regression else False
        self.mode = Mode.TRAIN

        self.class_id_list = {i: {} for i in range(self.num_classes)}
        self.input_dim = []
        cumulative_batch_size = 0
        self.num_examples = {}
        self.task_idxs = {}
        start_idx = 0
        self.scaler = MinMaxScaler()

        self.all_temps = np.concatenate([self.datasets[i][Mode.TRAIN]['data']['continuous'] for i in self.ENV], axis=0)
        self.scaler.fit(self.all_temps)
        if self.args.regression:
            for i in self.ENV:
                for type in [Mode.TRAIN, Mode.TEST_ID, Mode.TEST_OOD]:
                    self.datasets[i][type]['data']['continuous'] = self.scaler.transform(self.datasets[i][type]['data']['continuous'])

        for i in self.ENV:
            end_idx = start_idx + len(self.datasets[i][self.mode]['labels'])
            self.task_idxs[i] = [start_idx, end_idx]
            start_idx = end_idx

            for classid in range(self.num_classes):
                sel_idx = np.nonzero(self.datasets[i][self.mode]['labels'] == classid)[0]
                self.class_id_list[classid][i] = sel_idx
            print(f'Month {str(i)} loaded')

            self.num_examples[i] = len(self.datasets[i])

            cumulative_batch_size += min(self.mini_batch_size, self.num_examples[i])
            if args.method in ['erm']:
                self.input_dim.append((cumulative_batch_size, 123))
            else:
                self.input_dim.append((min(self.mini_batch_size, self.num_examples[i]), 123))


    def __getitem__(self, index):
        pass

    def __len__(self):
        pass

    def __str__(self):
        return 'precipitation'

    def update_historical(self, idx, data_del=False):
        time = self.ENV[idx]
        prev_time = self.ENV[idx - 1]
        self.datasets[time][self.mode]['data']['categorical'] = np.concatenate(
            (self.datasets[time][self.mode]['data']['categorical'], self.datasets[prev_time][self.mode]['data']['categorical']), axis=0)
        self.datasets[time][self.mode]['data']['continuous'] = np.concatenate(
            (self.datasets[time][self.mode]['data']['continuous'], self.datasets[prev_time][self.mode]['data']['continuous']), axis=0)
        self.datasets[time][self.mode]['labels'] = np.concatenate(
            (self.datasets[time][self.mode]['labels'], self.datasets[prev_time][self.mode]['labels']), axis=0)
        self.datasets[time][self.mode]['temperatures'] = np.concatenate(
            (self.datasets[time][self.mode]['temperatures'], self.datasets[prev_time][self.mode]['temperatures']), axis=0)
        if data_del:
            del self.datasets[prev_time]
        for classid in range(self.num_classes):
            sel_idx = np.nonzero(self.datasets[time][self.mode]['labels'] == classid)[0]
            self.class_id_list[classid][time] = sel_idx

    def update_historical_K(self, idx, K):
        time = self.ENV[idx]
        prev_time = self.ENV[idx - 1]
        self.window_start = self.ENV[max(0, idx - K)]
        if idx >= K:
            last_K_num_samples = self.input_dim[idx - K][0]
            self.datasets[time][self.mode]['data']['categorical'] = np.concatenate(
                (self.datasets[time][self.mode]['data']['categorical'],
                 self.datasets[prev_time][self.mode]['data']['categorical'][:-last_K_num_samples]), axis=0)
            self.datasets[time][self.mode]['data']['continuous'] = np.concatenate(
                (self.datasets[time][self.mode]['data']['continuous'],
                 self.datasets[prev_time][self.mode]['data']['continuous'][:-last_K_num_samples]), axis=0)
            self.datasets[time][self.mode]['labels'] = np.concatenate(
                (self.datasets[time][self.mode]['labels'], self.datasets[prev_time][self.mode]['labels'][:-last_K_num_samples]), axis=0)
            self.datasets[time][self.mode]['temperatures'] = np.concatenate(
                (self.datasets[time][self.mode]['temperatures'], self.datasets[prev_time][self.mode]['temperatures'][:-last_K_num_samples]), axis=0)
            del self.datasets[prev_time]
            for classid in range(self.num_classes):
                sel_idx = np.nonzero(self.datasets[time][self.mode]['labels'] == classid)[0]
                self.class_id_list[classid][time] = sel_idx
        else:
            self.update_historical(idx)

    def update_current_timestamp(self, time):
        self.current_time = time

    def get_lisa_new_sample(self, time_idx, classid, num_sample):
        # time = self.ENV[time_idx]
        idx_all = self.class_id_list[classid][time_idx]
        sel_idx = np.random.choice(idx_all, num_sample, replace=True)
        categorical_data = self.datasets[time_idx][self.mode]['data']['categorical'][sel_idx]
        continuous_data = self.datasets[time_idx][self.mode]['data']['continuous'][sel_idx]
        x = {}
        x['categorical'] = torch.FloatTensor(categorical_data).cuda()
        x['continuous'] = torch.FloatTensor(continuous_data).cuda()
        label = self.datasets[time_idx][self.mode]['labels'][sel_idx]

        return x, torch.LongTensor([label]).squeeze(0).unsqueeze(1).cuda()


class Precipitation(PrecipitationBase):
    def __init__(self, args):
        super().__init__(args=args)

    def __getitem__(self, index):
        if self.args.difficulty and self.mode == Mode.TRAIN:
            # Pick a time step from all previous timesteps
            idx = self.ENV.index(self.current_time)
            window = np.arange(0, idx + 1)
            sel_time = self.ENV[np.random.choice(window)]
            start_idx, end_idx = self.task_idxs[sel_time][self.mode]

            # Pick an example in the time step
            sel_idx = np.random.choice(np.arange(start_idx, end_idx))
            index = sel_idx

        categorical_data = self.datasets[self.current_time][self.mode]['data']['categorical'][index]
        continuous_data = self.datasets[self.current_time][self.mode]['data']['continuous'][index]
        x = {}
        x['categorical'] = torch.from_numpy(np.array(categorical_data))
        x['continuous'] = torch.from_numpy(continuous_data)
        if self.regression:
            label = self.datasets[self.current_time][self.mode]['temperatures'][index]
            return x, torch.FloatTensor([label])
        else:
            label = self.datasets[self.current_time][self.mode]['labels'][index]
            return x, torch.LongTensor([label])

    def __len__(self):
        return len(self.datasets[self.current_time][self.mode]['labels'])


class PrecipitationGroup(PrecipitationBase):
    def __init__(self, args):
        super().__init__(args=args)
        self.num_groups = args.num_groups
        self.group_size = args.group_size
        self.window_end = self.ENV[0]
        self.train = True
        self.groupnum = 0

    def __getitem__(self, index):
        if self.mode == Mode.TRAIN:
            np.random.seed(index)
            # Select group ID
            idx = self.ENV.index(self.current_time)
            if self.args.non_overlapping:
                possible_groupids = [i for i in range(0, max(1, idx - self.group_size + 1), self.group_size)]
                if len(possible_groupids) == 0:
                    possible_groupids = [np.random.randint(self.group_size)]
            else:
                possible_groupids = [i for i in range(max(1, idx - self.group_size + 1))]
            groupid = np.random.choice(possible_groupids)

            # Pick a time step in the sliding window
            window = np.arange(max(0, idx - groupid - self.group_size), idx + 1)
            sel_time = self.ENV[np.random.choice(window)]
            start_idx = self.task_idxs[sel_time][0]
            end_idx = self.task_idxs[sel_time][1]

            # Pick an example in the time step
            sel_idx = np.random.choice(np.arange(start_idx, end_idx))
            categorical_data = self.datasets[self.current_time][self.mode]['data']['categorical'][sel_idx]
            continuous_data = self.datasets[self.current_time][self.mode]['data']['continuous'][sel_idx]
            x = {}
            x['categorical'] = torch.from_numpy(np.array(categorical_data))
            x['continuous'] = torch.from_numpy(continuous_data)

            del window
            del sel_time
            del start_idx
            del end_idx

            if self.regression:
                label = self.datasets[self.current_time][self.mode]['temperatures'][sel_idx]
            else:
                label = self.datasets[self.current_time][self.mode]['labels'][sel_idx]

            return x, torch.LongTensor([label]), torch.LongTensor([groupid])

        else:
            categorical_data = self.datasets[self.current_time][self.mode]['data']['categorical'][index]
            continuous_data = self.datasets[self.current_time][self.mode]['data']['continuous'][index]
            x = {}
            x['categorical'] = torch.from_numpy(np.array(categorical_data))
            x['continuous'] = torch.from_numpy(continuous_data)
            if self.regression:
                label = self.datasets[self.current_time][self.mode]['temperatures'][index]
                return x, torch.FloatTensor([label])
            else:
                label = self.datasets[self.current_time][self.mode]['labels'][index]
                return x, torch.LongTensor([label])

    def group_counts(self):
        idx = self.ENV.index(self.current_time)
        return torch.LongTensor([1 for _ in range(min(self.num_groups, idx + 1))])

    def __len__(self):
        return len(self.datasets[self.current_time][self.mode]['labels'])