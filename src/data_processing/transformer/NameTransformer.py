class NameTransformer():
    def __init__(self):
        pass

    def transform(self, data):
        field_mapping = {
            'Ngay': 'Date',
            'GiaDieuChinh': 'AdjustedPrice',
            'GiaDongCua': 'Close',
            'ThayDoi': 'Change',
            'KhoiLuongKhopLenh': 'MatchedVolume',
            'GiaTriKhopLenh': 'MatchedValue',
            'KLThoaThuan': 'NegotiatedVolume',
            'GtThoaThuan': 'NegotiatedValue',
            'GiaMoCua': 'Open',
            'GiaCaoNhat': 'High',
            'GiaThapNhat': 'Low',
        }

        # Rename the columns
        data.rename(columns=field_mapping, inplace=True)
        return data