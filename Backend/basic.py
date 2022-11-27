def successResponse(code=200, detail="success", data=None):
    '''
    返回成功的响应
    @params: code:int 状态码, detail:str 返回信息, data:Object 数据
    @return: dict
    '''
    return {
        "code": code,
        "detail": detail,
        "data": data
    }


def failResponse(code=400, detail="failed", data=None):
    '''
    返回失败的响应
    @params: code:int 状态码, detail:str 返回信息, data:Object 数据
    @return: dict
    '''
    return {
        "code": code,
        "detail": detail,
        "data": data
    }