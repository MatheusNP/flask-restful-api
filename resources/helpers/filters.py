
def normalize_path_params(
    city = None,
    grade_min = 0,
    grade_max = 5,
    daily_min = 0,
    daily_max = 10000,
    limit = 50,
    offset = 0,
    **data
):
    if city:
        return {
            'grade_min': grade_min,
            'grade_max': grade_max,
            'daily_min': daily_min,
            'daily_max': daily_max,
            'city': city,
            'limit': limit,
            'offset': offset
        }
    return {
        'grade_min': grade_min,
        'grade_max': grade_max,
        'daily_min': daily_min,
        'daily_max': daily_max,
        'limit': limit,
        'offset': offset
    }

sql_wout_city = " SELECT * FROM hotels \
                    WHERE grade BETWEEN ? AND ? \
                    AND daily BETWEEN ? AND ? \
                    LIMIT ? OFFSET ?"

sql_with_city = " SELECT * FROM hotels \
                    WHERE grade BETWEEN ? AND ? \
                    AND daily BETWEEN ? AND ? \
                    AND city = ? \
                    LIMIT ? OFFSET ?"