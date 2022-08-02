function register() {
  $.ajax({
    type: "POST",
    url: "/api/register",
    data: {
      id_give: $('#userid').val(),
      pw_give: $('#userPw').val(),
      nickname_give: $('#userNick').val()
    },
    success: function (response) {
      if (response['result'] == 'success') {
        alert('회원가입이 완료되었습니다.')
        window.location.href = '/login'
      } else {
        alert(response['msg'])
      }
    }
  })
}