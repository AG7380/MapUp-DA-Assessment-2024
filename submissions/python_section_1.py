from typing import Dict, List
import pandas as pd

#Q1
def reverse_by_n_elements(lst: List[int], n: int) -> List[int]:
    result = []
    for i in range(0, len(lst), n):
        temp = []
        for j in range(min(n, len(lst) - i)):
            temp.insert(0, lst[i + j])
        result.extend(temp)
    lst[:] = result
    return lst

#Q2
def group_by_length(lst: List[str]) -> Dict[int, List[str]]:
    length_dict = {}    
    for string in lst:
        length = len(string)  
        if length not in length_dict:  
            length_dict[length] = []  
        length_dict[length].append(string)  
    dict = {k: length_dict[k] for k in sorted(length_dict)}  
    return dict

#Q3
def flatten_dict(nested_dict: Dict, sep: str = '.') -> Dict:
    dict_result = {}
    stack = [(nested_dict, '')]

    while stack:
        curr_dict, parent_key = stack.pop()

        if isinstance(curr_dict, dict):
            for key, value in curr_dict.items():
                new_key = f"{parent_key}{sep}{key}" if parent_key else key
                if isinstance(value, dict):
                    stack.append((value, new_key))
                elif isinstance(value, list):
                    for i, item in enumerate(value):
                        stack.append((item, f"{new_key}[{i}]"))
                else:
                    dict_result[new_key] = value
        elif isinstance(curr_dict, list):
            for i, item in enumerate(curr_dict):
                stack.append((item, f"{parent_key}[{i}]"))

    return dict_result

#Q4
def unique_permutations(nums: List[int]) -> List[List[int]]:
    nums.sort()
    result = []
    used = [False] * len(nums)

    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return
        
        for i in range(len(nums)):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            
            used[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            used[i] = False

    backtrack([])
    return result

#Q5
def find_all_dates(text: str) -> List[str]:
    date_formats = [
        r'\b\d{2}-\d{2}-\d{4}\b',
        r'\b\d{2}/\d{2}/\d{4}\b',
        r'\b\d{4}\.\d{2}\.\d{2}\b'
    ]
    
    combined_formats = '|'.join(date_formats)
    result = re.findall(combined_formats, text)
    
    return result

#Q6
def polyline_to_dataframe(polyline_str: str) -> pd.DataFrame:
    coords = polyline.decode(polyline_str)
    df = pd.DataFrame(coords, columns=['latitude', 'longitude'])
    df['distance'] = 0.0

    for i in range(1, len(df)):
        lat1, lon1 = df.loc[i-1, 'latitude'], df.loc[i-1, 'longitude']
        lat2, lon2 = df.loc[i, 'latitude'], df.loc[i, 'longitude']
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        r = 6371000
        df.loc[i, 'distance'] = r * c

    return df

#Q7
def rotate_and_transform_matrix(mat: List[List[int]]) -> List[List[int]]:
    size = len(mat)
    rotated = [[0] * size for _ in range(size)]
    
    for r in range(size):
        for c in range(size):
            rotated[c][size-1-r] = mat[r][c]

    final = [[0] * size for _ in range(size)]

    for r in range(size):
        for c in range(size):
            row_sum = sum(rotated[r]) - rotated[r][c]
            col_sum = sum(rotated[k][c] for k in range(size)) - rotated[r][c]
            final[r][c] = row_sum + col_sum

    return final


#Q8
import pandas as pd

def time_check(df: pd.DataFrame) -> pd.Series:
    date_format = "%Y-%m-%d" 
    time_format = "%H:%M:%S" 

    df['start'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format=f"{date_format} {time_format}", errors='coerce')
    df['end'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format=f"{date_format} {time_format}", errors='coerce')

    grouped = df.groupby(['id', 'id_2'])
    results = []

    starting_date = pd.Timestamp('2024-01-01')

    for (id_val, id_2_val), group in grouped:
        days_covered = set()

        for day_offset in range(7):
            day_start = starting_date + pd.Timedelta(days=day_offset)
            day_end = day_start + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

            day_data = group[(group['start'] <= day_end) & (group['end'] >= day_start)]
            
            if not day_data.empty and (day_data['start'].min() <= day_start) and (day_data['end'].max() >= day_end):
                days_covered.add(day_start.date())

        all_days_covered = len(days_covered) == 7
        full_24_hour_coverage = (group['end'].max() - group['start'].min()).total_seconds() >= 24 * 3600

        results.append((id_val, id_2_val, not (all_days_covered and full_24_hour_coverage)))

    result_series = pd.Series({(id_val, id_2_val): incorrect for id_val, id_2_val, incorrect in results})
    result_series.index = pd.MultiIndex.from_tuples(result_series.index, names=['id', 'id_2'])

    return result_series
