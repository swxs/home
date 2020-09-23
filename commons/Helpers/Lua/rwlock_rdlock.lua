--[[
    # None：加锁成功
    # 数字n：n(ms)后锁释放
--]]
local write_key = 'write'
local mode = redis.call('hget', KEYS[1], 'mode')
if (mode == false) then
    redis.call('hset', KEYS[1], 'mode', 'read')
    redis.call('hset', KEYS[1], write_key, 0)
    redis.call('hset', KEYS[1], ARGV[2], 1)
    redis.call('pexpire', KEYS[1], ARGV[1])
    return nil
end
if (mode == 'read') then
    local ind = redis.call('hincrby', KEYS[1], ARGV[2], 1)
    local remainTime = redis.call('pttl', KEYS[1])
    redis.call('pexpire', KEYS[1], math.max(remainTime, ARGV[1]))
    return nil
end
return redis.call('pttl', KEYS[1])
