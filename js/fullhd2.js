let site = {
    host: "https://www.baidu.to",
    headers: {
        "User-Agent": MOBILE_UA,
        "Accept": "text/html",
        "accept-language": "zh-CN,zh;q=0.8"
    },
    encoding: "UTF-8",
    sniffer: false,
    isVideo: ".mp4#.m3u8#.flv#video/tos",
    play_json: [],

    // 首页
    homeUrl: "https://www.baidu.to/zh",
    home: async function () {
        // 硬编码分类：最新&最佳&热门
        const cats = [
            { type_name: "最新", type_id: "latest-updates" },
            { type_name: "最佳", type_id: "top-rated" },
            { type_name: "热门", type_id: "most-popular" }
        ];
        return cats;
    },

    homeVod: async function () {
        let url = this.homeUrl;
        let htmlText = await request(url);
        let $ = html(htmlText);
        let list = [];
        $('a.thumb_img').each((i, el) => {
            let title = $(el).attr('title') || '';
            let detUrl = $(el).attr('href') || '';
            // 图片拼接逻辑
            let pic = '';
            let m = detUrl.match(/videos\/(\d+)/);
            if(m){
                let vid = m[1];
                let dir1 = Math.floor(Number(vid) / 10000) * 10000;
                pic = `https://img.fullhd.to/${dir1}/${vid}/small/1.jpg`;
            }
            // 副标题 替换
            let subTitle = $(el).find('span.duration').text() || '';
            subTitle = subTitle.replace('完整视频','时长');

            list.push({
                vod_id: detUrl,
                vod_name: title,
                vod_pic: pic,
                vod_remarks: subTitle
            })
        })
        return { list }
    },

    // 分类列表  tid: latest‑updates / top‑rated / most‑popular
    category: async function(tid, pg) {
        let url = `${this.host}/zh/${tid}/${pg}/`;
        let htmlText = await request(url);
        let $ = html(htmlText);
        let list = [];
        $('a.thumb_img').each((i, el) => {
            let title = $(el).attr('title') || '';
            let detUrl = $(el).attr('href') || '';
            let pic = '';
            let m = detUrl.match(/videos\/(\d+)/);
            if(m){
                let vid = m[1];
                let dir1 = Math.floor(Number(vid) / 10000) * 10000;
                pic = `https://img.baidu.to/${dir1}/${vid}/small/1.jpg`;
            }
            let subTitle = $(el).find('span.duration').text() || '';
            subTitle = '时长' + subTitle;

            list.push({
                vod_id: detUrl,
                vod_name: title,
                vod_pic: pic,
                vod_remarks: subTitle
            })
        })
        return {
            list,
            page: pg,
            pagecount: 999
        }
    },

    // 详情页
    detail: async function(vidUrl) {
        let htmlText = await request(vidUrl);
        let $ = html(htmlText);
        let playFrom = ["默认线路"];
        let playUrlList = [];

        $('video source').each((i, el) => {
            let label = $(el).attr('label') || `第${i+1}集`;
            let src = $(el).attr('src') || '';
            playUrlList.push(`${label}$${src}`);
        })
        // 原配置：是否反转选集序列=1
        playUrlList = playUrlList.reverse();

        return {
            vod_name: "",
            vod_content: "",
            vod_play_from: playFrom.join("$$$"),
            vod_play_url: playUrlList.join("#")
        }
    },

    // 播放解析，直链直接返回
    play: async function(flag, id) {
        return {
            parse:0,
            url:id,
            jx:0
        }
    },

    // 搜索，原配置无搜索规则返回空
    search: async function(kw, pg) {
        return { list:[] }
    }
}

// 导出给drpy2.1引擎调用
export default site;
