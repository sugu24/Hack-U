// ------------------ Ajax設定 ------------------ //
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// ------------------ 終了 ------------------ //
var post_count = 0
var bulletinBoard = document.getElementById('bulletinBoard')
var good_stamp = new Set()
var bad_stamp = new Set()
var delete_stock = new Set()

var createMassData = function(id, name, response, postdate, content, good, bad){
    //console.log(id, name, response, date, content, good, bad)
    var insertHTML = '<div class="mass_data" id="' + id + '">'
    insertHTML += '<div class="info"><span class="name">' + id + ' . ' + name + '</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="time">' + postdate + ' </span> </div>'
    insertHTML += '<div class="content">'
    if(response != "")insertHTML += '<div>' + response + ' >>></div>'
    insertHTML += '<div>' + content + '</div>'
    insertHTML += '</div>'
    insertHTML += '<div class="function">'
    insertHTML += '<a href="#post_container" class="response" id="response' + id + '">返信</a>'
    insertHTML += '<div class="good"><button class="btn btn_good" id="good' + id + '" type="submit" name="good' + id + '">○</button><span class="good_number" id="good_number_show' + id + '">' + good + '</span></div>'
    insertHTML += '<div class="bad"><button class="btn btn_bad" id="bad' + id + '" type="submit" name="post_btn' + id + '">×</button><span class="bad_number" id="bad_number_show' + id + '">' + bad + '</span></div>'
    insertHTML += '</div>'
    insertHTML += '</div>'
    document.getElementById('bulletinBoard').innerHTML += insertHTML
    return
}


var getPostsData = function(){
    $.ajax({
        'url': '',
        'type': 'POST',
        'data': {'type': 'getPostsData','after': post_count},
        'dataType': 'json',
        success: function(response){
            var post_datas = response.post_datas
            for (var i = 0; i < post_datas.length; i++){
                createMassData(post_datas[i]["post_id"],post_datas[i]["name"],post_datas[i]["response_post_id"],post_datas[i]["postdate"],post_datas[i]["content"],post_datas[i]["good"],post_datas[i]["bad"])
            }
            post_count += i
            if(i === 100)getPostsData()
        }
    })
}

$('#update_form').on('submit', function(e) {
    e.preventDefault()
    getPostsData()
})

$('#delete').on('click', function(e){
    e.preventDefault()
    for(var delete_element of delete_stock){
        document.getElementById(delete_element).remove()
    }
    post_count -= delete_stock.size
    delete_stock = new Set()
    document.getElementById('delete').style.visibility = "hidden"
})

$('#post_form').on('submit', function(e) {
    e.preventDefault()
    document.getElementById('error').innerText = ""
    var name = document.getElementById('post_name').value
    var content = document.getElementById('post_content').value
    var response = document.getElementById('response_id').value
    if (name.length > 40 && content.length > 200){
        document.getElementById("error").innerText = "名前と投稿文が40文字と200文字を超えています\n現在、名前"+name.length+"字・投稿文"+content.length+"字"　
        return
    }
    else if(name.length > 40){
        document.getElementById("error").innerText = "名前が40文字を超えています\n現在、名前"+name.length+"字"
        return
    }
    else if(content.length > 200){
        document.getElementById("error").innerText = "投稿文が200文字を超えています\n現在  投稿文"+content.length+"字"
        return
    }
    document.getElementById('error').innerText = ""
    var date = new Date()
    time = date.getFullYear() + "/" + (date.getMonth()+1) + "/" + date.getDate() + " " + date.getHours() + ":" + date.getMinutes()
    $.ajax({
        'url': '',
        'type': 'POST',
        'data': {'type': 'setPostData', 'name': name, 'content': content, 'time':time, 'response': response},
        'dataType': 'json'
    })
    .done(function(response){
        if(response.error != "")document.getElementById('error').innerText = response.error
        else getPostsData()
    })
})

$(document).on('click', '.response',function(){
    var id = $(this).attr('id')
    for (var i = id.length; id[i-1].charCodeAt(0) >= 48 && id[i-1].charCodeAt(0) <= 57; i--){}
    document.getElementById('response_id').value = id.slice(i,id.length)
})

$(document).on('click', '.btn_good', function(){
    var id = $(this).attr('id')
    for (var i = id.length; id[i-1].charCodeAt(0) >= 48 && id[i-1].charCodeAt(0) <= 57; i--){}
    var post_id = id.slice(i,id.length)
    var action = ""
    if(!good_stamp.has(id)){
        good_stamp.add(id)
        action = 'plus'
    }
    else{
        good_stamp.delete(id)
        action = 'minus'
    }
    $.ajax({
        'url': '',
        'type': 'POST',
        'data': {'type': 'good_action', 'post_id': post_id, 'action': action},
        'dataType': 'json'
    })
    .done(function(esponse){
        if(action == "plus"){
            document.getElementById('good_number_show'+String(post_id)).style.color = "red"
            document.getElementById('good_number_show'+String(post_id)).style.fontWeight = "bold"
        }else if(action == "minus"){
            document.getElementById('good_number_show'+String(post_id)).style.color = ""
            document.getElementById('good_number_show'+String(post_id)).style.fontWeight = ""
        }
    })
})

$(document).on('click', '.btn_bad', function(){
    var id = $(this).attr('id')
    for (var i = id.length; id[i-1].charCodeAt(0) >= 48 && id[i-1].charCodeAt(0) <= 57; i--){}
    var post_id = id.slice(i,id.length)
    var action = ""
    if(!bad_stamp.has(id)){
        bad_stamp.add(id)
        action = 'plus'
    }
    else{
        bad_stamp.delete(id)
        action = 'minus'
    }
    $.ajax({
        'url': '',
        'type': 'POST',
        'data': {'type': 'bad_action', 'post_id': post_id, 'action': action},
        'dataType': 'json'
    })
    .done(function(response){
        if(action == "plus"){
            document.getElementById('bad_number_show'+String(post_id)).style.color = "blue"
            document.getElementById('bad_number_show'+String(post_id)).style.fontWeight = "bold"
        }else if(action == "minus"){
            document.getElementById('bad_number_show'+String(post_id)).style.color = ""
            document.getElementById('bad_number_show'+String(post_id)).style.fontWeight = ""
        }
    })
})

// onload時に残りのPOSTを受信
window.onload = function(){
    post_count = $(".mass_data").length
    if(post_count === 100) 
        getPostsData()
}

// ----------- websocket ----------- //
var roomName = document.getElementById('thread_name_span').innerText

var dataSocket = new WebSocket(
    "ws://"
    + window.location.host
    + '/ws/'
    + roomName
    +'/'
)

dataSocket.onmessage = function(e) {
    const data = JSON.parse(e.data)
    if (data.flag == "good_action"){
        document.getElementById('good_number_show'+String(data.post_id)).innerText = data.number
    }else if(data.flag == "bad_action"){
        document.getElementById('bad_number_show'+String(data.post_id)).innerText = data.number
    }else if(data.flag == "delete_action"){
        if(data.response != null){
            for(var object of data.response){
                delete_stock.add(String(object["post_id"]))
                document.getElementById(String(object["post_id"])).style.color = "#00000042"
            }
        }
        delete_stock.add(String(data.delete))
        document.getElementById(String(data.delete)).style.color = "#00000042"
        document.getElementById('delete').style.visibility = "visible"
    }
};

dataSocket.onclose = function(e) {
    alert('リアルタイム通信がタイムアウトになりました。\nリロードしてください');
};