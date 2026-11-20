var rule = {
    title:'fullhd',
    host:'https://www.fullhd.to',
    //homeUrl:'/zh',
    url:'/fyclass/fypage/[/fyclass/]',
    searchUrl:'/search/**/',
    searchable:2,
    headers:'User-Agent$MOBILE_UA#Referer$https://www.fullhd.to#Accept$text/html,image/jpeg,*/*#Accept-Language$zh-CN,zh;q=0.8',
    timeout:5000,
    class_url:'latest-updates&top-rated&most-popular&networks/brazzers-com&networks/tushy-com&networks/naughtyamerica-com&sites/sexmex&sites/passion-hd&categories/animation&categories/18-years-old&categories/pawg&categories/thong&categories/stockings&categories/jav-uncensored&categories/pantyhose',
    class_name:'最新&最佳&热门&Brazzers&Tushy&NaughtyA&Sexmex&Passion&动画&18岁&丰臀女孩&丁字裤&丝袜&日本未审查&连裤袜',
    //class_name:'#page-viewport&&ul&&li;.text&&Text;a&&href;/(.*)',
    cate_exclude:'应用',
    //推荐:'a.thumb_img;pd(this,"&&title","测试标题");img&&src;span.duration&&Text;a&&href',
一级:`js:
let htmlText = getHtml(MY_URL);
let arr = [];
let searchPos = 0;
while(true){
    let posThumb = htmlText.indexOf('class="thumb_img"', searchPos);
    if(posThumb === -1){
        break;
    }
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
        // ========== 从href路径 /videos/后面截取数字ID，切掉末尾3位 ==========
        let objId = "";
        let imgSrc = "";
        if(href){
            let key = "/videos/";
            let sPos = href.indexOf(key);
            if(sPos !== -1){
                let idStart = sPos + key.length;
                let ePos = href.indexOf("/", idStart);
                if(ePos !== -1){
                    objId = href.substring(idStart, ePos);
                    //if(objId.length >= 3){
                    //    objId = objId.substring(0, objId.length - 3);
                    //}
                }
            }
            // ⚠️务必替换为站点真实图片URL模板
            if(objId){
                imgSrc = "https://img.fullhd.to/"+objId.substring(0, objId.length - 3)+"000/"+objId+"/small/1.jpg";
    // 请求图片，带上referer
    //let imgBin = getBinary(imgSrc);//, {
    //    headers:{
   //         "Referer":"https://www.fullhd.to"
    //    }
    //})
    // 二进制转 base64
    //let b64 = toBase64(imgBin);
    //vod_pic = "data:image/jpeg;base64," + b64;
            }
        }
        // duration（副标题）
        let mDur = aBlock.match(/<span class="duration">(.*)span>/);
        let dur = "";
        if(mDur){
            dur = mDur[1];
                    if(dur.length > 3){
                        dur = dur.substring(0, dur.length - 2);
                    }
let keyword = "Full Video";
let pos = dur.indexOf(keyword);
if(pos !== -1){
    // 截取 Full Video 之后的全部字符串
    dur = dur.substring(pos + keyword.length);
    // 可选：清理开头多余空格，优化显示效果
    while(dur.length > 0 && dur.charAt(0) === " "){
        dur = dur.substring(1);
    }
}
        }
        arr.push({
            vod_name: title,
            vod_pic: imgSrc,
            vod_remarks: dur,
            vod_id:href
        });
    }
    // 更新下一轮搜索起点，向后移动，防止死循环
    searchPos = posAEnd + 4;
}
VODS = arr;
`,

    double:false,
    limit:50,
    //play_parse:true,
    //一级:'a.thumb_img;pd(this,"&&title","测试标题");img&&src;span.duration&&Text;href',
    推荐:"*",
    //二级:';;;;;video;source&&label;source&&src',
二级:`js:
log("二级开始执行，MY_URL="+MY_URL);
let pageUrl = MY_URL;
let pageHtml = "";
try{
    pageHtml = getHtml(pageUrl);
}catch(e){
    log("getHtml报错："+e);
}

//这里替换成你解析video、source代码，组装播放数组
let vod = {
    title:"测试",
    img:"",
    vod_play_data:[
        {
            name:"测试线路720P",
            urls:"正片$https://www.w3schools.com/html/mov_bbb.mp4"
        }
    ]
};
//直接返回完整vod对象，不再送入嗅探、不再进lazy！！
return vod;
`,
    搜索:'a.thumb_img;&&title;img&&src;span.duration&&Text;&&href',
}
