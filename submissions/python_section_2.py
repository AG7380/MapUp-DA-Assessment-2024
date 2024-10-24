import pandas as pd
import numpy as np
import datetime

#Q9
def calculate_distance_matrix(df) -> pd.DataFrame():
    toll_ids = pd.concat([df['id_start'], df['id_end']]).unique()
    distance_matrix = pd.DataFrame(np.inf, index=toll_ids, columns=toll_ids, dtype=float)
    np.fill_diagonal(distance_matrix.values, 0)
    
    for _, row in df.iterrows():
        source = row['id_start']
        destination = row['id_end']
        distance = row['distance']
        distance_matrix.at[source, destination] = distance
        distance_matrix.at[destination, source] = distance

    for k in toll_ids:
        for i in toll_ids:
            for j in toll_ids:
                if distance_matrix.at[i, j] > distance_matrix.at[i, k] + distance_matrix.at[k, j]:
                    distance_matrix.at[i, j] = distance_matrix.at[i, k] + distance_matrix.at[k, j]
    
    return distance_matrix


#Q10
def unroll_distance_matrix(df) -> pd.DataFrame:
    unrolled_data = []

    for id_start in df.index:
        for id_end in df.columns:
            if id_start != id_end:
                distance = df.at[id_start, id_end]
                unrolled_data.append([id_start, id_end, distance])

    unrolled_df = pd.DataFrame(unrolled_data, columns=['id_start', 'id_end', 'distance'])

    return unrolled_df


#Q11
def find_ids_within_ten_percentage_threshold(df, reference_id) -> pd.DataFrame:
    reference_avg_distance = df[df['id_start'] == reference_id]['distance'].mean()
    threshold_floor = reference_avg_distance * 0.9
    threshold_ceiling = reference_avg_distance * 1.1
    
    matching_ids = []
    
    for id_start in df['id_start'].unique():
        avg_distance = df[df['id_start'] == id_start]['distance'].mean()
        if threshold_floor <= avg_distance <= threshold_ceiling:
            matching_ids.append(id_start)
    
    return sorted(matching_ids)


#Q12
def calculate_toll_rate(df) -> pd.DataFrame:
    df['moto'] = df['distance'] * 0.8
    df['car'] = df['distance'] * 1.2
    df['rv'] = df['distance'] * 1.5
    df['bus'] = df['distance'] * 2.2
    df['truck'] = df['distance'] * 3.6
    
    return df


#Q13
def calculate_time_based_toll_rates(df) -> pd.DataFrame:
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    time_ranges = [
        (datetime.time(0, 0), datetime.time(10, 0), 0.8),
        (datetime.time(10, 0), datetime.time(18, 0), 1.2),
        (datetime.time(18, 0), datetime.time(23, 59, 59), 0.8)
    ]

    new_rows = []

    for _, row in df.iterrows():
        for day in days:
            for start_time, end_time, weekday_discount in time_ranges:
                new_row = row.copy()

                new_row['start_day'] = day
                new_row['end_day'] = day
                new_row['start_time'] = start_time
                new_row['end_time'] = end_time

                if day in ['Saturday', 'Sunday']:
                    discount = 0.7
                else:
                    discount = weekday_discount

                for vehicle in ['moto', 'car', 'rv', 'bus', 'truck']:
                    new_row[vehicle] *= discount
                
                # Convert id_start and id_end to integers
                new_row['id_start'] = int(new_row['id_start'])
                new_row['id_end'] = int(new_row['id_end'])

                new_rows.append(new_row)

    result_df = pd.DataFrame(new_rows)

    result_df = result_df[['id_start', 'start_time', 'start_day', 'id_end', 'end_time', 'end_day', 'distance', 'moto', 'car', 'rv', 'bus', 'truck']]
    
    return result_df

