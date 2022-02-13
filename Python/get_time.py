from datetime import datetime, timedelta, timezone

def get_utc():
    UTC = timezone(timedelta(hours=0),"UTC")
    return UTC

def get_ect():
    ECT = timezone(timedelta(hours=+1),"ECT")
    return ECT

def get_eet():
    EET = timezone(timedelta(hours=+2),"EET")
    return EET

def get_art():
    ART = timezone(timedelta(hours=+2),"ART")
    return ART

def get_eat():
    EAT = timezone(timedelta(hours=+3),"EAT")
    return EAT

def get_met():
    MET = timezone(timedelta(hours=+3,minutes=+30),"MET")
    return MET

def get_net():
    NET = timezone(timedelta(hours=+4),"NET")
    return NET

def get_plt():
    PLT = timezone(timedelta(hours=+5) ,"PLT")
    return PLT

def get_ist():
    IST = timezone(timedelta(hours=+5,minutes=+30),"IST")
    return IST

def get_bst():
    BST = timezone(timedelta(hours=+6),"BST")
    return BST

def get_vst():
    VST = timezone(timedelta(hours=+7),"VST")
    return VST

def get_cct():
    CCT = timezone(timedelta(hours=+8),"CCT")
    return CCT

def get_jst():
    JST = timezone(timedelta(hours=+9),"JST")
    return JST

def get_act():
    ACT = timezone(timedelta(hours=+9,minutes=+30),"ACT")
    return ACT

def get_aet():
    AET = timezone(timedelta(hours=+10),"AET")
    return AET

def get_sst():
    ACT = timezone(timedelta(hours=+11),"ACT")
    return ACT

def get_nst():
    NST = timezone(timedelta(hours=+12),"ACT")
    return NST

def get_mit():
    MIT = timezone(timedelta(hours=-11),"MIT")
    return MIT

def get_hit():
    HIT = timezone(timedelta(hours=-10),"HIT")
    return HIT

def get_ast():
    AST = timezone(timedelta(hours=-9),"AST")
    return AST

def get_pst():
    PST = timezone(timedelta(hours=-8),"PST")
    return PST

def get_pnt():
    PNT = timezone(timedelta(hours=-7),"PNT")
    return PNT

def get_mst():
    AST = timezone(timedelta(hours=-7),"AST")
    return AST

def get_cst():
    CST = timezone(timedelta(hours=-6),"CST")
    return CST

def get_est():
    EST = timezone(timedelta(hours=-5),"EST")
    return EST

def get_iet():
    IET = timezone(timedelta(hours=-5),"IET")
    return EST

def get_prt():
    PRT = timezone(timedelta(hours=-4),"EST")
    return PRT

def get_cnt(): 
    CNT = timezone(timedelta(hours=-3,minutes=-30),"CNT")
    return CNT

def get_agt():
    AGT = timezone(timedelta(hours=-3),"AGT")
    return AGT

def get_bet():
    BET = timezone(timedelta(hours=-3),"BET")
    return BET

def get_cat():
    CAT = timezone(timedelta(hours=-1),"CAT")
    return CAT