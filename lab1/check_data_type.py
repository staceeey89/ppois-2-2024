def check_data_type(cur_data_type, need_data_type):
    if cur_data_type is not need_data_type:
        raise TypeError()
