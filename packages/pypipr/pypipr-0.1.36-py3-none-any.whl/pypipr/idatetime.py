import re
import datetime


class idatetime:
    regex_for_parse_input = r"(?:\d|\w|\-|\+|\:|\.|\'|\/)+"

    timestamp_regex = r"\d{10,22}"

    date_year_front = "(\d{3,4})"
    date_year_back = "(\d{1,4})"
    date_month = r"(0?[1-9]|1[012]|(?:jan(?:uary)?)|(?:feb(?:ruary)?)|(?:mar(?:ch)?)|(?:apr(?:il)?)|may|(?:ju(?:ne?|ly?))|(?:aug(?:ust)?)|(?:sep(?:tember)?)|(?:oct(?:ober)?)|(?:(?:nov|dec)(?:ember)?))"
    date_day = r"(0?[1-9]|[12][0-9]|3[01])"
    date_separator = "[^a-zA-Z0-9:]+"
    date_regex = rf"(?:{date_year_front}{date_separator})?(?:{date_month}{date_separator})?{date_day}(?(2)|{date_separator}{date_month})?(?(1)|{date_separator}{date_year_back})?"

    time_hour_24 = r"([01]?\d|2[0-4])"
    time_hour_12 = "(0?\d|1[012])"
    time_minute = r"([0-5]?\d)"
    time_second = r"([0-5]?\d)"
    time_milisecond = r"(\d{3,9})"
    time_am = "([ap]m)"
    time_separator = "(?:[^a-zA-Z0-9\/\-]+)"
    time_regex = rf"(?:{time_hour_12}|{time_hour_24})(?:(?:{time_separator}{time_minute})(?:{time_separator}{time_second}(?:{time_separator}{time_milisecond})?)?)?(?(1){time_separator}?{time_am})?"

    year_regex = r"(\d{4}|\'\d{2})"

    list_regex = {
        "timestamp": timestamp_regex,
        "date": date_regex,
        "time": time_regex,
        "tzinfo": r"",
        "year": year_regex,
        "month": date_month,
        "day": date_day,
        "hour": time_hour_24,
        "minute": time_minute,
        "second": time_second,
        "microsecond": time_milisecond,
    }

    list_month = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]

    def __init__(
        self,
        human_string_datetime,
        default_year=1900,
        default_month=1,
        default_day=1,
        overwrite=None,
    ):
        """
        Membuat idatetime object dengan input teks yg mengandung unsur waktu dan tanggal.
        defaul_*    : digunakan untuk mengisikan nilai awal
        overwrite   : digunakan untuk mengubah hasil proses menjadi datetime yg di khususkan

        contoh:
        self.overwrite_date= {
            "tzinfo": int type,
            "year": int type,
            "month": int type,
            "day": int type,
            "hour": int type,
            "minute": int type,
            "second": int type,
            "microsecond": int type,
        }
        """

        self.result = {
            "tzinfo": [],
            "year": [],
            "month": [],
            "day": [],
            "hour": [],
            "minute": [],
            "second": [],
            "microsecond": [],
        }

        self.default_date = {
            "year": default_year,
            "month": default_month,
            "day": default_day,
        }

        self.overwrite_date = overwrite if overwrite else {}

        for text in self.parse_string(human_string_datetime):
            for index, value in self.list_regex.items():
                if r := re.fullmatch(value, text, re.IGNORECASE):
                    r = self.sanitize_regex_result(r)
                    if n := getattr(self, f"parse_{index}")(r):
                        for i, v in n.items():
                            self.result[i].append(v)

    def to_datetime(self):
        """
        Return idatetime menjadi python standard library datetime object.

        Langkah:
        - Python datetime memerlukan Year, Month, Day untuk diisikan, jadi digunakan
            default year, month, day
        - Kemudian diupdate dengan data hasil proses program
        - Kemudian diupdate kembali dengan data overwrite yg diinputkan
        """
        d = self.default_date
        c = {x: y[0] for x, y in self.result.items() if y}
        d.update(c)
        d.update(self.overwrite_date)
        return datetime.datetime(**d)

    def parse_string(self, s):
        """
        Parse string yg diinput.
        Parse menjadi bagian-bagian perkata.
        """
        return re.findall(self.regex_for_parse_input, s)

    def sanitize_regex_result(self, r):
        """
        Menjadikan hasil regex sesuai dengan type nya.
        """
        result = []
        for x in r.groups():
            try:
                v = x if x is not None else 0
                v = float(x)
                v = int(x)
            except:
                pass
            result.append(v)
        return result

    def parse_tzinfo(self, r):
        pass

    def parse_date(self, r):
        if all(
            {
                year := r[0] or r[4],
                month := r[1] or r[3],
                day := r[2],
            }
        ):
            # return {"year": year, "month": month, "day": day}
            return (
                self.parse_year([year])
                | self.parse_month([month])
                | self.parse_day([day])
            )
        return None

    def parse_time(self, r):
        return {
            "hour": r[0] or r[1],
            "minute": r[2],
            "second": r[3],
            "microsecond": r[4],
        }

    def parse_year(self, r):
        return {"year": r[0]}

    def parse_month(self, r):
        month = r[0]
        if type(month_str := month) is str:
            for i, v in enumerate(self.list_month, 1):
                if v.startswith(month_str.lower()):
                    month = i
        return {"month": month}

    def parse_day(self, r):
        return {"day": r[0]}

    def parse_hour(self, r):
        return {"hour": r[0]}

    def parse_minute(self, r):
        return {"minute": r[0]}

    def parse_second(self, r):
        return {"second": r[0]}

    def parse_microsecond(self, r):
        return {"microsecond": r[0]}
