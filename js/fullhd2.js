let site = {
    host: "https://www.fullhd.to",
    headers: {
        "User-Agent": MOBILE_UA,
        "Accept": "text/html",
        "accept-language": "zh-CN,zh;q=0.8"
    },
    encoding: "UTF-8",
    sniffer: false,
    isVideo: ".mp4#.m3u8#.flv#video/tos",
    play_json: [],
    homeUrl: "https://www.fullhd.to/zh",

    // 【公共工具：由详情url生成封面地址】统一一处维护图片域名
    genPic(detUrl) {
        if (!detUrl) return "";
        const IMG_HOST = "https://img.fullhd.to";
        const m = detUrl.match(/videos\/(\d+)/);
        if (!m) return "";
        const vid = Number(m[1]);
        const dir1 = Math.floor(vid / 10000) * 10000;
        return `${IMG_HOST}/${dir1}/${vid}/small/1.jpg`;
    },

    home: async function () {
        // 硬编码分类：最新&最佳&热门
        const cats = [
            { type_name: "最新", type_id: "latest‑updates" },
            { type_name: "最佳", type_id: "top‑rated" },
            { type_name: "热门", type_id: "most‑popular" }
        ];
        return cats;
    },

    homeVod: async function () {
        try {
            const url = this.homeUrl;
            const htmlText = await request(url);
            const $ = html(htmlText);
            const list = [];
            $("a.thumb_img").each((i, el) => {
                const title = $(el).attr("title") || "";
                const detUrl = $(el).attr("href") || "";
                const pic = this.genPic(detUrl);

                let subTitle = $(el).find("span.duration").text() || "";
                subTitle = subTitle.replace("完整视频", "时长");

                list.push({
                    vod_id: detUrl,
                    vod_name: title,
                    vod_pic: pic,
                    vod_remarks: subTitle
                });
            });
            console.log(`homeVod 获取条目:${list.length}`);
            return { list };
        } catch (e) {
            console.log("homeVod异常：", e.message);
            return { list: [] };
        }
    },

    category: async function (tid, pg) {
        try {
            const url = `${this.host}/zh/${tid}/${pg}/`;
            const htmlText = await request(url);
            const $ = html(htmlText);
            const list = [];
            $("a.thumb_img").each((i, el) => {
                const title = $(el).attr("title") || "";
                const detUrl = $(el).attr("href") || "";
                const pic = this.genPic(detUrl);

                let subTitle = $(el).find("span.duration").text() || "";
                subTitle = "时长" + subTitle;

                list.push({
                    vod_id: detUrl,
                    vod_name: title,
                    vod_pic: pic,
                    vod_remarks: subTitle
                });
            });
            console.log(`category tid=${tid} pg=${pg} 获取条目:${list.length}`);
            return {
                list,
                page: pg,
                pagecount: 999
            };
        } catch (e) {
            console.log("category异常：", e.message);
            return { list: [], page: pg, pagecount: 0 };
        }
    },

    detail: async function (vidUrl) {
        try {
            const htmlText = await request(vidUrl);
            const $ = html(htmlText);
            const playFrom = ["默认线路"];
            const playUrlList = [];

            $("video source").each((i, el) => {
                const label = $(el).attr("label") || `第${i + 1}集`;
                const src = $(el).attr("src") || "";
                if (src) {
                    playUrlList.push(`${label}$${src}`);
                }
            });
            // 是否反转选集序列=1
            playUrlList.reverse();

            return {
                vod_name: "",
                vod_content: "",
                vod_play_from: playFrom.join("$$$"),
                vod_play_url: playUrlList.join("#")
            };
        } catch (e) {
            console.log("detail异常：", e.message);
            return {
                vod_name: "",
                vod_content: "详情解析失败",
                vod_play_from: "默认线路",
                vod_play_url: ""
            };
        }
    },

    play: async function (flag, id) {
        return {
            parse: 0,
            url: id,
            jx: 0
        };
    },

    search: async function (kw, pg) {
        return { list: [] };
    }
};

export default site;
