--[[
    # None：加锁成功
    # 数字n：n(ms)后锁释放
--]]
local write_key = 'write'
local mode = redis.call('hget', KEYS[1], 'mode')
if (mode == false) then
    redis.call('hset', KEYS[1], 'mode', 'write')
    redis.call('hset', KEYS[1], write_key, 1)
    redis.call('pexpire', KEYS[1], ARGV[1])
    return nil
end
if (mode == 'read') then
    if (redis.call('hexists', KEYS[1], write_key) == 1) then
        redis.call('hincrby', KEYS[1], write_key, -1)
        return redis.call('pttl', KEYS[1])
    end
end
if (mode == 'write') then
    if (redis.call('hexists', KEYS[1], write_key) == 1) then
        redis.call('hincrby', KEYS[1], write_key, 1)
        local currentExpire = redis.call('pttl', KEYS[1])
        redis.call('pexpire', KEYS[1], currentExpire + ARGV[1])
        return redis.call('pttl', KEYS[1])
    end
end
return redis.call('pttl', KEYS[1])
