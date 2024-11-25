local http = require("socket.http")
local ltn12 = require("ltn12")
local json = require("dkjson")

local function load_standard(filename)
    local file = io.open(filename, "r")
    if not file then
        error("Could not open file: " .. filename)
    end
    local content = file:read("*all")
    file:close()
    return json.decode(content)
end

local function test_api(test)
    local url = test.url
    local method = test.method:upper()
    local headers = test.headers or {}
    local payload = test.body and json.encode(test.body) or ""
    local query_params = test.query_params or {}
    local weight = test.weight or 0

    -- Construct query string
    local query_string = ""
    for k, v in pairs(query_params) do
        query_string = query_string .. k .. "=" .. v .. "&"
    end
    if query_string ~= "" then
        query_string = "?" .. query_string:sub(1, -2)
    end

    -- Prepare request
    local response_body = {}
    local request = {
        url = url .. query_string,
        method = method,
        headers = headers,
        source = ltn12.source.string(payload),
        sink = ltn12.sink.table(response_body)
    }

    -- Send request
    local res, code, response_headers, status = http.request(request)
    if not res then
        print("Score: 0\nReason: " .. code)
        return 0
    end

    -- Check status code
    local expected_status = test.response.status
    if code ~= expected_status then
        print("Score: 0\nReason: Expected status code " .. expected_status .. ", but got " .. code)
        return 0
    end

    -- Check response body
    local response_json = table.concat(response_body)
    local data, pos, err = json.decode(response_json, 1, nil)
    if err then
        print("Score: 0\nReason: Response is not a valid JSON")
        return 0
    end

    local expected_body = test.response.body
    for key, value in pairs(expected_body) do
        if data[key] ~= value then
            print("Score: 0\nReason: Expected '" .. key .. "' to be '" .. value .. "', but got '" .. tostring(data[key]) .. "'")
            return 0
        end
    end

    return weight
end

local function main()
   if #arg ~= 1 then
        print("Usage: lua autograder-lua.lua <standard.json>")
        os.exit(1)
    end
    local standard_file = arg[1]
    local standard = load_standard(standard_file)
    local total_score = 0
    local max_score = 0

    for _, test in ipairs(standard.tests) do
        max_score = max_score + (test.weight or 0)
        total_score = total_score + test_api(test)
    end

    print("Total Score: " .. total_score .. "/" .. max_score)
end

main()