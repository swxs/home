--[[
    # None：释放成功
    # 0：释放失败
    # 1：释放成功，且锁释放
--]]
local write_key = 'write'
local mode = redis.call('hget', KEYS[1], 'mode')
if (mode == false) then
    return 1
end
local lockExists = redis.call('hexists', KEYS[1], write_key)
if (lockExists == 0) then
    return nil
end
local counter = redis.call('hincrby', KEYS[1], ARGV[1], -1)
if (counter == 0) then
    redis.call('hdel', KEYS[1], ARGV[1])
end
if (redis.call('hlen', KEYS[1]) > 2) then
    if mode == 'write' then
        return 0
    end
    return nil
end
redis.call('del', KEYS[1])
return 1
