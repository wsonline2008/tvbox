var rule = {
    title:'fullhd',
    host:'https://www.fullhd.to',
    homeUrl:'/zh',
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
    推荐:'body;a.thumb_img;title;img&&src;span.duration&&Text;href',
    double:true,
    limit:5,
    play_parse:false,
    //一级:'a.thumb_img;title;img&&src;span.duration&&Text;href',
    一级:`js:
    let htmlText = getHtml(MY_URL);
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
    二级:{
        title: "",          // 片名选择器
        img: "",       // 详情页封面
        desc: "类型:span.type&&Text;年份:span.year&&Text;地区:span.area&&Text;更新:span.update&&Text",
        content:".intro&&Text",     // 简介
        tabs:"",       // 线路/标签外层容器
        lists:"",   // 每一条线路对应的选集容器，#id会自动替换线路下标
        tab_text:"",      // 线路名称文本提取
        list_text:"source&&label",       // 单集的集数名称
        list_url:"source&&src",         // 单集播放链接
        重定向:""             // 拿到详情html之后执行js，可以返回新html
    },
    搜索:'a.thumb_img;title;img&&src;span.duration&&Text;href',
}
