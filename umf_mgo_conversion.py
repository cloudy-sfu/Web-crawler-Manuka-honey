umf_0 = 25
max_iteration = 6  # mgo = 0 requires 6 iteration


def umf_to_mgo(umf: int):
    # ref: https://www.umf.org.nz/unique-manuka-factor/
    return round(-0.0106763961 * umf**3 + 1.76329448 * umf**2 + 11.0752267 * umf - 15.1796541)


def umf_to_mgo_d1(umf: int):
    # root (Newton-Raphson cannot converge): 113.16116396, -3.05568995
    return -0.0320291883 * umf**2 + 3.52658896 * umf + 11.0752267


def mgo_to_umf(mgo: float):
    umf = umf_0  # tested, don't need to wrap `copy`
    for i in range(max_iteration):
        mgo_0 = umf_to_mgo(umf) - mgo
        if abs(mgo_0) < 1e-6:
            break
        mgo_0_d1 = umf_to_mgo_d1(umf)
        umf = umf - mgo_0 / mgo_0_d1
    return round(umf)
