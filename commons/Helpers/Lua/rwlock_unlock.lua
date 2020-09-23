--[[
    # 0：释放失败
# 1：释放成功，且锁释放
--]]
if (redis.call('hget', KEYS[1], 'mode') == 'read') or (redis.call('hget', KEYS[1], 'mode') == 'write') then
    redis.call('del', KEYS[1])
    return 1
end
return 0
