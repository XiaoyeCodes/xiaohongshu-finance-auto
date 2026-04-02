#!/usr/bin/env node
/**
 * 小红书财经 - 4 月 3 日：搞钱副业分享
 */

const { Client } = require('@modelcontextprotocol/sdk/client/index.js');
const { StreamableHTTPClientTransport } = require('@modelcontextprotocol/sdk/client/streamableHttp.js');
const path = require('path');

async function publishFinance() {
    const serverUrl = new URL('http://localhost:18060/mcp');
    let client;
    
    // 问答式文案
    const title = '下班后做什么能多赚 3000？这 5 个副业靠谱';
    
    const content = `Q：上班族有什么副业推荐？
A：这是我被问最多的问题

先说结论：
别碰刷单、点赞、打字员
那些都是割韭菜的

我做过的 5 个靠谱副业：

1️⃣ 知识付费（最推荐）
把你的专业技能包装成课程
我上过班的朋友做了 Excel 课
一个月卖 30 份，每份 199
被动收入 6000/月

平台：小红书/知乎/得到
启动成本：时间（录课）
适合人群：有一技之长的

2️⃣ 自媒体写作
给公众号/知乎写稿
一篇 800-3000 不等
我刚开始写 800/篇
后来稳定 2000/篇
一个月写 4 篇=8000

平台：公众号投稿/知乎盐选
启动成本：0
适合人群：喜欢写作的

3️⃣ 技能接单
设计/剪辑/翻译/编程
我在猪八戒接过 UI 设计
一单 2000-5000
一个月接 2 单=5000+

平台：猪八戒/一品威客/淘宝
启动成本：作品集
适合人群：有硬技能的

4️⃣ 电商无货源
一件代发，赚差价
我朋友做拼多多无货源
一个月利润 3000-8000
但需要选品和运营

平台：拼多多/1688
启动成本：1000-3000 保证金
适合人群：有时间的

5️⃣ 线下兼职
周末家教/活动执行/探店
我大学时做过家教
150/小时，周末 4 小时=600
一个月 2400

平台：BOSS 直聘/豆瓣小组
启动成本：0
适合人群：时间灵活的

【我的副业收入变化】

2020 年：0（不知道能做什么）
2021 年：800/月（开始写稿）
2022 年：3500/月（接设计单）
2023 年：8000/月（课程 + 稿费）
2024 年：12000/月（稳定渠道）

【给新手的建议】

1. 先别辞职，用业余时间试
2. 选能积累的，别做一次性
3. 前期别投钱，用时间换经验
4. 找到正反馈再加大投入

副业不是赚快钱
是给自己多一条路

有想做的可以评论区说
帮你分析靠不靠谱～

#副业 #搞钱 #技能变现 #上班族副业 #副业推荐 #个人成长 #90 后理财 #被动收入 #自媒体 #知识付费`;

    try {
        console.log('发布财经笔记...');
        
        client = new Client({
            name: 'xhs-finance',
            version: '1.0.0',
        }, {
            capabilities: { tools: {} },
        });
        
        const transport = new StreamableHTTPClientTransport(serverUrl);
        await client.connect(transport);
        
        // 使用今天生成的配图
        const localImagePath = 'C:\\Users\\danwe\\.qclaw\\workspace\\2026-04-02-10-39-48-an-infographic-poster-for-xiaohongshu.png';
        
        console.log('正在发布...');
        console.log('配图:', localImagePath);
        
        const result = await client.callTool({
            name: 'publish_content',
            arguments: {
                title: title,
                content: content,
                images: [localImagePath],
            },
        });
        
        console.log('结果:', JSON.stringify(result, null, 2));
        
        if (result.isError) {
            return false;
        }
        
        return true;
        
    } catch (error) {
        console.error('错误:', error.message);
        return false;
    } finally {
        if (client) {
            await client.close();
        }
    }
}

(async () => {
    const success = await publishFinance();
    console.log(success ? '✅ 成功' : '❌ 失败');
    process.exit(success ? 0 : 1);
})();
