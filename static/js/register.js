// 아이디 정규표현식
function is_nickname(asValue) {
  var regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{2,10}$/
  return regExp.test(asValue)
}

function is_password(asValue) {
  var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/
  return regExp.test(asValue)
}


// 아이디 중복 클라
function check_dup() {
  let username = $('#id_title').val()
  console.log(username)
  if (username == '') {
    $('#help-id').text('아이디를 입력해주세요.').removeClass('is-safe').addClass('is-danger')
    $('#input-username').focus()
    return
  }
  if (!is_nickname(username)) {
    $('#help-id').text('아이디의 형식을 확인해주세요. 영문과 숫자, 일부 특수문자(._-) 사용 가능. 2-10자 길이').removeClass('is-safe').addClass('is-danger')
    $('#input-username').focus()
    return
  }
  $('#help-id').addClass('is-loading')
  $.ajax({
    type: 'POST',
    url: '/sign_up/check_dup',
    data: {
      username_give: username,
    },
    success: function (response) {
      if (response['exists']) {
        $('#help-id').text('이미 존재하는 아이디입니다.').removeClass('is-safe').addClass('is-danger')
        $('#input-username').focus()
      } else {
        $('#help-id').text('사용할 수 있는 아이디입니다.').removeClass('is-danger').addClass('is-success')
      }
      $('#help-id').removeClass('is-loading')
    },
  })
}

// 비밀번호 같은지 확인
function same_pw() {
  let pw = $('#userPw').val()
  let pw2 = $('userPw2').val()
  
}

// 회원가입
// function register() {
//   $.ajax({
//     type: 'POST',
//     url: '/api/register',
//     data: {
//       id_give: $('#userid').val(),
//       nickname_give: $('#userNick').val(),
//       pw_give: $('#userPw').val(),
//       pw2_give: $('#userPw2').val(),
//     },
//     success: function (response) {
//       if (response['result'] == 'success') {
//         alert('회원가입이 완료되었습니다.')
//         window.location.href = '/login'
//       } else {
//         alert(response['msg'])
//       }
//     },
//   })
// }
