// const homeURL = 
$('form').on('submit', function (e) {
    e.preventDefault();
    var form = $(this);
    const comment = form.find('textarea').val();
    if (!comment){
        console.log('comment is empty')
        return
    }
    $.ajax({
        url: form.attr('action'),
        type: 'POST',
        data: form.serialize(),
        success: function (response) {
            if (response.status === "unauthenticated") {
                window.location.replace(form.attr('homeURL'))
            }
            if (response.status === "success") {
                form.find('textarea').val('');
                const comment = response.comment;
                const commentDiv = `
                <div class="card my-2">
                    <div class="card-header">
                        <h5>${ comment.user_id__username }</h5>
                        <span>${ comment.created_at }</span>
                    </div>
                    <div class="card-body">
                        <p>${ comment.comment }</p>
                    </div>
                </div>
                `
                $('.comments').prepend(commentDiv);
            }
        },
        error: function (error) {
            console.log(error)
        }
    })
})

$('a.likeBtn').on('click', function (e) {
    e.preventDefault();
    const btn = $(this);
    $.ajax({
        url: btn.attr('href'),
        type: 'GET',
        success: function (response) {
            console.log(response)
            if (response.status === "unauthenticated") {
                window.location.replace(btn.attr('homeURL'))
            }
            if (response.status === "success") {
                $('#likesShow').text(`Likes: ${response.likes}`);
            }
        },
        error: function (error) {
            console.log(error)
        }
    })
})