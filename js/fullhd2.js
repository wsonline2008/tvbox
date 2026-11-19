var rule = {
    title:'fullhd',
    host:'https://www.fullhd.to/zh',
    //homeUrl:'/zh',
    url:'[/fyclass/]fyclass/fypage',
    searchUrl:'/search/**',
    searchable:2,
    headers:{
        'User-Agent':'MOBILE_UA'
    },
    timeout:5000,
    class_url:'latest-updates&top-rated&most-popular',
    class_name:'最新&最佳&热门',
    //class_name:'#page-viewport&&ul&&li;.text&&Text;a&&href;/(.*)',
    cate_exclude:'应用',
    推荐:'a.thumb_img;title;img&&src;span.duration&&Text;href',
    double:false,
    limit:50,
    play_parse:false,
    //一级:'a.thumb_img;title;img&&src;span.duration&&Text;href',
    一级:`js:
    let htmlText = getHtml(input);
    let $ = html(htmlText);
let arr=[];
$("a.thumb_img").each((i,el)=>{
    arr.push({
        vod_id: $(el).attr("href") || "",
        vod_name: $(el).attr("title") || "",
        vod_pic: $(el).find("img").attr("src") || "",
        vod_remarks: $(el).find("span.duration").text() || "",
        vod_year: "2026",
        vod_area: "内地",
        vod_actor: "张三",
        vod_content: "这是剧情简介"
    })
});
    VODS = arr; //一级/推荐js模式赋值VODS，不要VOD
    `,


    //二级:';;;;;video;source&&label;source&&src',
二级:`js:
let htmlText = getHtml(input);
let $ = html(htmlText);
let sourceArr = [];

// 取出video下面全部source标签
$("video source").each((i, el)=>{
    let src = $(el).attr("src") || "";
    let label = $(el).attr("label") || "";
    if(src){ // 过滤空地址
        sourceArr.push({
            text: label,
            url: src
        })
    }
});
// =========核心：数组反向排序=========
sourceArr.reverse();
// 拼接成格式：集名$播放地址#集名$播放地址
let playListStr = sourceArr.map(item=>{
    return item.text + "$" + item.url;
}).join("#");

VOD = {
    vod_name: "",       //片名按需填写，留空就""
    vod_pic: "",        //封面，按需从页面抓取
    vod_remarks: "",
    vod_content: "从video-source抓取，已经反向排序",
    vod_play_from: "默认线路",  //线路名称，多条线路可以继续扩展
    vod_play_url: playListStr
};
console.log("反向后的选集列表：", playListStr);
`,
    搜索:'a.thumb_img;title;img&&src;span.duration&&Text;href',
}
