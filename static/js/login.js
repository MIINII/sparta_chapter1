function sign_up() {
    window.location.href = '/register'
}

function sign_in() {
  let username = $('#input-username').val()
  let password = $('#input-password').val()

  if (username == '' || password == '') {
    $('#help-id').text('아이디를 입력해주세요.').focus().removeClass('is-safe').addClass('is-danger')
    $('#help-password').text('비밀번호를 입력해주세요.').focus().removeClass('is-safe').addClass('is-danger')
    $('#input-username')
    return
  } else {
    $('#help-id, #help-password').text('')
  }

  $.ajax({
    type: 'POST',
    url: '/login/sign_in',
    data: {
      username_give: username,
      password_give: password,
    },
    success: function (response) {
      if (response['result'] == 'success') {
        $.cookie('mytoken', response['token'], { path: '/main' })
        window.location.href = '/main'
      } else {
        alert(response['msg'])
      }
    },
  })
}
