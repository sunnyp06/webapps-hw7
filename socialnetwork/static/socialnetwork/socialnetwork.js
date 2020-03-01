// Sends a new request to update the to-do list
function refresh_page() {
    site_name = $('#id_name_of_page').text()
    console.log(site_name)
    if (site_name == "Global Stream") 
        {query_url = "/socialnetwork/refresh-global"}
    else if (site_name == "Follower Stream") 
        {query_url = "/socialnetwork/refresh-follower"}
    else {return}

    $.ajax({
        type: "GET",
        url: query_url,
        dataType : "json",
        data: {"last_refresh": last_refresh},
        success: update_page
    });
}

function update_page(items) {

    // $("[id^='startsWith']")

    // for post, prepend post, create comment section
    // for comment, find #post_comments_[post_id], append comment with rel info
    console.log(items)
    console.log(items.comments)
    
    $(items.posts).each(function (){add_post(this);})
    $(items.comments).each(function () {add_comment(this);})
    last_refresh = items.last_refresh
}

function add_post(post) {
    post_id = post.id
    text = sanitize(post.text)
    user_name = post.user_name
    post_time = post.post_time
    full_name = post.full_name
    // $('#all_posts').prepend("this is a test")
    $('#all_posts').prepend(
                '<div>' +
                    '<td>Post by <a href="profile/' + user_name + '" id="id_post_profile_' + post_id + '">' + full_name + '</a> </td>' +
                    '<td> <span id="id_post_text_' + post_id + '"> ' + text + ' </span></td>' +
                    '<td> <span id="id_post_date_time_' + post_id + '">' + post_time + '</span> </td>' +
                '<!-- for each comment on this post, create row -->' +
                '<div id="post_comments_' + post_id + '">' +
                '</div>' +
                '<!-- new comment input -->' +
                '<tr><div class="comment">' +
                    '<td>New Comment:</td>' +
                    '<td> <input type="text" id="id_comment_input_text_' + post_id + '" name="post_text"> </td>' +
                    '<td> <button type="submit" onclick=new_comment(' + post_id + ') id="id_comment_button_' + post_id + '">Submit</button> </td>' +
                '</div></div>')
}

function add_comment(comment) {
    post_id = comment.post_id
    comment_id = comment.id
    text = sanitize(comment.text)
    user_name = comment.user_name
    comment_time = comment.comment_time
    full_name = comment.full_name
    $('#post_comments_' + post_id).append(
                '<div>' +
                    '<td>Comment by <a href="profile/' + user_name + '" id="id_comment_profile_' + comment_id + '">' + full_name + '</a> </td>' +
                    '<td> <span id="id_comment_text_' + comment_id + '"> ' + text + ' </span></td>' +
                    '<td> <span id="id_comment_date_time_' + comment_id + '">' + comment_time + '</span> </td>' +
                '</div>')
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
}

function displayError(message) {
    $("#error").html(message);
}

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        c = cookies[i].trim();
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length);
        }
    }
    return "unknown";
}

function new_comment(post_id) {
    var input_element = $('#id_comment_input_text_' + post_id);
    var comment_text = input_element.val();


    // Clear input box and old error message (if any)
    input_element.val('');
    displayError('');

    $.ajax({
        url: "/socialnetwork/add-comment",
        type: "POST",
        data: {'comment_text': comment_text, 
               'csrfmiddlewaretoken': getCSRFToken(),
               'post_id': post_id},
        dataType : "json"
    });
    
    refresh_page();
}


last_refresh = "2005-02-17 18:16:13.615598+00:00";
// The index.html does not load the list, so we call refresh_page()
// as soon as page is finished loading
window.onload = refresh_page;

// causes list to be re-fetched every 5 seconds
window.setInterval(refresh_page, 5000);
