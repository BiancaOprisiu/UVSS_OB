import re

def check_cnp_is_valid(cnp):
    return list(map(check_cnp_is_valid_unvec, cnp))

def check_cnp_is_valid_unvec(cnp):
    if cnp is None:
        msg = "This value is missing"
        print(msg)
        return None

    if not isinstance(cnp, int):
        msg = f"CNP should be a number. You supplied a {type(cnp)}."
        print(msg)
        return False

    if len(str(cnp)) != 13:
        msg = f"CNP is made up of 13 digits. You supplied a number made up of {len(str(cnp))} digits."
        print(msg)
        return False

    cnp_dec = decompose_cnp(cnp)

    if cnp_dec["S"] not in map(str, range(1, 9)):
        msg = f"The 'S' component - first digit - should be between 1 and 8. Your number has {cnp_dec['S']} as first digit."
        print(msg)
        return False

    valid_months = [str(month).zfill(2) for month in range(1, 13)]

    if cnp_dec["LL"] not in valid_months:
        msg = f"The months component ('LL') should be between 01 and 12. The 'LL' component for your number is {cnp_dec['LL']}."
        print(msg)
        return False

    cnp_month = int(cnp_dec["LL"])

    max_days_in_month = {
        1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }

    if int(cnp_dec["ZZ"]) > max_days_in_month[cnp_month]:
        msg = f"The 'ZZ' component should not be more than {max_days_in_month[cnp_month]} - the maximum number of days in {cnp_month}. The 'ZZ' component for your number is {cnp_dec['ZZ']}."
        print(msg)
        return False

    checksum = get_cnp_checksum(cnp)

    if checksum != int(cnp_dec["C"]):
        print("The checksum does not match the expected value.")
        return False

    return True

def decompose_cnp(cnp):
    cnp_str = str(cnp)
    return {
        "S": cnp_str[0],
        "LL": cnp_str[3:5],
        "ZZ": cnp_str[5:7],
        "C": cnp_str[12]
    }

def get_cnp_checksum(cnp):
    cnp_str = str(cnp)
    weights = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]
    checksum = sum(int(cnp_str[i]) * weights[i] for i in range(12)) % 11
    return 1 if checksum == 10 else checksum

# Example usage:
cnp_list = [1234567890123, 1234567890124, 2940921324815, 6020528324792]  # List of CNP numbers
results = check_cnp_is_valid(cnp_list)
print(results)
