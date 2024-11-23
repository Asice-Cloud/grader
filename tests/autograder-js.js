const axios = require('axios');
const fs = require('fs');

function loadStandard(filename) {
    const data = fs.readFileSync(filename, 'utf8');
    return JSON.parse(data);
}

async function testApi(test) {
    const url = test.url;
    const method = test.method.toUpperCase();
    const headers = test.headers || {};
    const payload = test.body || {};
    const queryParams = test.query_params || {};
    const weight = test.weight || 0;

    let response;
    try {
        if (method === 'GET') {
            response = await axios.get(url, { headers, params: queryParams });
        } else if (method === 'POST') {
            response = await axios.post(url, payload, { headers, params: queryParams });
        } else if (method === 'PUT') {
            response = await axios.put(url, payload, { headers, params: queryParams });
        } else if (method === 'DELETE') {
            response = await axios.delete(url, { headers, data: payload, params: queryParams });
        } else {
            console.log(`Unsupported HTTP method: ${method}`);
            return 0;
        }
    } catch (error) {
        console.log(`Score: 0\nReason: ${error.message}`);
        return 0;
    }

    // 检查响应状态码
    const expectedStatus = test.response.status;
    if (response.status !== expectedStatus) {
        console.log(`Score: 0\nReason: Expected status code ${expectedStatus}, but got ${response.status}`);
        return 0;
    }

    // 检查响应是否为JSON
    const data = response.data;
    const expectedBody = test.response.body;
    for (const key in expectedBody) {
        if (data[key] !== expectedBody[key]) {
            console.log(`Score: 0\nReason: Expected '${key}' to be '${expectedBody[key]}', but got '${data[key]}'`);
            return 0;
        }
    }

    return weight;
}

async function main() {
    standardFile = "./tests/standard.json"
    const standard = loadStandard(standardFile);
    let totalScore = 0;
    let maxScore = 0;

    for (const test of standard.tests) {
        maxScore += test.weight || 0;
        totalScore += await testApi(test);
    }

    console.log(`Total Score: ${totalScore}/${maxScore}`);
}

main();