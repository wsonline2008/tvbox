var rule = {
    title:'fullhd',
    host:'https://www.fullhd.to',
    homeUrl:'https://www.fullhd.to/zh',
    url:'/zh/fyclass/fypage/',
    detailUrl:'',
    searchUrl:'',
    searchable:0,
    headers:{
        'User-Agent':'MOBILE_UA',
        'Accept':'text/html',
        'accept-language':'zh-CN,zh;q=0.8'
    },
    timeout:5000,
    // 硬编码分类：最新&最佳&热门 对应标识 latest‑updates&top‑rated&most‑popular
    class_name:'最新&最佳&热门',
    class_url:'latest-updates&top-rated&most-popular',
    cate_exclude:'',
    // 首页推荐 js模式，a.thumb_img数组，图片通过href正则拼接
    推荐:'js:{\
        let htmlText = getHtml(MY_URL);\
        let $ = html(htmlText);\
        let arr = [];\
        $("a.thumb_img").each((i,el)=>{\
            let title = $(el).attr("title")||"";\
            let detUrl = $(el).attr("href")||"";\
            let vod_remarks = $(el).find("span.duration").text()||"";\
            vod_remarks = vod_remarks.replace("完整视频","时长");\
            let pic = "";\
            let m = detUrl.match(/videos\\/(\\d+)/);\
            if(m){\
                let vid = m[1];\
                let dir1 = Math.floor(Number(vid)/10000)*10000;\
                pic = `https://img.fullhd.to/${dir1}/${vid}/small/1.jpg`;\
            }\
            arr.push({vod_name:title,vod_id:detUrl,vod_pic:pic,vod_remarks:vod_remarks});\
        });\
        VODS = arr;\
    }',
    double:false,
    limit:20,
    // 一级分类列表 js模式
    一级:'js:{\
        let htmlText = getHtml(MY_URL);\
        let $ = html(htmlText);\
        let arr = [];\
        $("a.thumb_img").each((i,el)=>{\
            let title = $(el).attr("title")||"";\
            let detUrl = $(el).attr("href")||"";\
            let vod_remarks = $(el).find("span.duration").text()||"";\
            vod_remarks = "时长"+vod_remarks;\
            let pic = "";\
            let m = detUrl.match(/videos\\/(\\d+)/);\
            if(m){\
                let vid = m[1];\
                let dir1 = Math.floor(Number(vid)/10000)*10000;\
                pic = `https://img.fullhd.to/${dir1}/${vid}/small/1.jpg`;\
            }\
            arr.push({vod_name:title,vod_id:detUrl,vod_pic:pic,vod_remarks:vod_remarks});\
        });\
        VODS = arr;\
    }',
    // 二级详情 js模式，解析video>source选集，反转选集顺序
    二级:'js:{\
        let htmlText = getHtml(MY_URL);\
        let $ = html(htmlText);\
        let playFrom = ["默认线路"];\
        let playUrlList = [];\
        $("video source").each((i,el)=>{\
            let label = $(el).attr("label")||`第${i+1}集`;\
            let src = $(el).attr("src")||"";\
            playUrlList.push(`${label}$${src}`);\
        });\
        playUrlList = playUrlList.reverse();\
        VOD = {\
            vod_name:"",\
            vod_content:"",\
            vod_play_from:playFrom.join("$$$"),\
            vod_play_url:playUrlList.join("#")\
        };\
    }',
    // 原配置无搜索，返回空列表
    搜索:'js:{VODS=[];}',
    play_parse:false,
    sniffer:false,
    isVideo:".mp4#.m3u8#.flv#video/tos"
}
