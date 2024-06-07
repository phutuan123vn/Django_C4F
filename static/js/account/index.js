$('button#toggle-SignIn').click(function () {
    $('.container-form').removeClass('active')
})
$('button#toggle-SignUp').click(function (event) {
    console.log(event.target)
    $('.container-form').addClass('active')
})

function addInvalidDiv(message) {
    const invalidDiv = document.createElement('div')
    invalidDiv.className = 'invalid-feedback'
    const content = message.reduce((acc, curr) => acc + curr + '<br>', '')
    invalidDiv.innerHTML = content
    return invalidDiv
  }
// Fetch all the forms we want to apply custom Bootstrap validation styles to
$('input.inputValue').on('keydown', function (event) {
    event.target.classList.remove('is-invalid')
})

$('form.form-signUp').on('submit', function (event) {
    event.preventDefault()
    formData = new FormData()
    formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val())
    formData.append('username', $('input[name="username"].input-signUp').val())
    formData.append('password', $('input[name="password"].input-signUp').val())
    formData.append('conf-pass', $('input[name="conf-pass"].input-signUp').val())
    $.ajax({
        url: '/account/',
        type: 'POST',
        enctype: 'multipart/form-data',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {
            event.preventDefault()
            if (data.hasOwnProperty('status') && data['status'] === 'success') {
                event.target.submit()
            }
            // $('form').addClass('was-validated')
            // $('div.invalid-feedback').remove()
            if (data.hasOwnProperty('password2')){
                const message = data['password2']
                $('input[name="password"].input-signUp').after(addInvalidDiv(message))
                $('input[name="conf-pass"].input-signUp').after(addInvalidDiv(message))
                $('input[name="password"].input-signUp').addClass('is-invalid')
                $('input[name="conf-pass"].input-signUp').addClass('is-invalid')
            }
            if (data.hasOwnProperty('username')){
                const message = data['username']
                $('input[name="username"].input-signUp').after(addInvalidDiv(message))
                $('input[name="username"].input-signUp').addClass('is-invalid')
            }
            },
            error: function (data) {
                console.log("error")
                console.log(data)
            }
    })
})

$('form.form-signIn').on('submit', function (event) {
    event.preventDefault()
    console.log($('input[name="username"].input-signIn').val())
    console.log($('input[name="password"].input-signIn').val())
    formData = new FormData()
    formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val())
    formData.append('username', $('input[name="username"].input-signIn').val())
    formData.append('password', $('input[name="password"].input-signIn').val())
    console.log(formData)
    $.ajax({
        url: '/account/login/',
        type: 'POST',
        enctype: 'multipart/form-data',
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function(res) {
            console.log(res)
            if (res.hasOwnProperty('status') && res['status'] === 'success') {
                event.target.submit()
            }
            if (res.hasOwnProperty('status') && res['status'] === 'error') {
                $('input[name="username"].input-signIn').addClass('is-invalid')
                $('input[name="password"].input-signIn').addClass('is-invalid')
                $('input[name="username"].input-signIn').after(addInvalidDiv(['Invalid username or password']))
                $('input[name="password"].input-signIn').after(addInvalidDiv(['Invalid username or password']))
            }
        },
        error: function (res) {
            console.log("error")
            console.log(res)
        }
    })
})