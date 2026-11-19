var rule = {
    title:'fullhd',
    host:'https://www.fullhd.to',
    homeUrl:'/zh',
    url:'/fyclass/',
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
    //推荐:'a.thumb_img;pd(this,"&&title","测试标题");img&&src;span.duration&&Text;a&&href',
推荐:`js:
let htmlText = getHtml(MY_URL);
let arr = [];
let posThumb = htmlText.indexOf('class="thumb_img"');
let posAStart = htmlText.lastIndexOf('<a ', posThumb);
let posAEnd = htmlText.indexOf('</a>', posThumb);

if(posThumb !== -1 && posAStart !== -1 && posAEnd !== -1){
    let aBlock = htmlText.substring(posAStart, posAEnd + 4);
    // href
    let mHref = aBlock.match(/href\s*=\s*["']([^"']+)["']/);
    let href = "";
    if(mHref){
        href = mHref[1];
    }
    // title
    let mTitle = aBlock.match(/title\s*=\s*["']([^"']+)["']/);
    let title = "无标题";
    if(mTitle){
        title = mTitle[1];
    }
    // data‑src 图片
    let mImg = aBlock.match(/data-src\s*=\s*["']([^"']+)["']/);
    let imgSrc = "";
    if(mImg){
        imgSrc = mImg[1];
    }
    // duration
    let mDur = aBlock.match(/<span class="duration">(.*)span>/);
    let dur = "";
    if(mDur){
        dur = mDur[1];
    }
    arr.push({
        vod_name: title,
        vod_pic: imgSrc,
        vod_remarks: dur,
        vod_id:href
    });
}
if(arr.length === 0){
    arr.push({
        vod_name:"⚠未捕获",
        vod_remarks:"posThumb="+posThumb+" | posAStart="+posAStart+" | posAEnd="+posAEnd,
        vod_id:"#err"
    });
}
VODS = arr;
`,
    double:false,
    limit:50,
    play_parse:false,
    //一级:'a.thumb_img;pd(this,"&&title","测试标题");img&&src;span.duration&&Text;href',
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
    });
});
    VODS = arr; //一级/推荐js模式赋值VODS，不要VOD
    `,


    //二级:';;;;;video;source&&label;source&&src',
    二级:{
        title: "1",          // 片名选择器
        img: "",       // 详情页封面
        desc: "类型",
        content:"简介",     // 简介
        tabs:"body",       // 线路/标签外层容器
        lists:"video",   // 每一条线路对应的选集容器，#id会自动替换线路下标
        tab_text:"线路",      // 线路名称文本提取
        list_text:"source&&label",       // 单集的集数名称
        list_url:"source&&src",         // 单集播放链接
        重定向:""             // 拿到详情html之后执行js，可以返回新html
    },
    搜索:'a.thumb_img;&&title;img&&src;span.duration&&Text;&&href',
}
