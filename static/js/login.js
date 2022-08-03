function sign_up() {
    window.location.href = '/register'
}

function sign_in() {
  let userid = $('#input-id').val()
  let password = $('#input-password').val()

  if (userid == '' || password == '') {
    $('#help-id').text('아이디를 입력해주세요.').focus().removeClass('is-safe').addClass('is-danger')
    $('#help-password').text('비밀번호를 입력해주세요.').focus().removeClass('is-safe').addClass('is-danger')
    $('#input-username')
    return
  } else {
    $('#help-id, #help-password').text('')
  }

  $.ajax({
    type: 'POST',
    url: '/sign_in',
    data: {
      userid_give: userid,
      password_give: password,
    },
    success: function (response) {
      if (response['result'] == 'success') {
        $.cookie('mytoken', response['token'], {path: '/'});
        window.location.href = '/main'
      } else {
        alert(response['msg'])
      }
    },
  })
}
