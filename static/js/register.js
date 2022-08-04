function sign_in() {
  window.location.href = '/login'
}

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
  let username = $('#userid').val()

  if (username == '') {
    $('#help-id').text('⚠ 아이디를 입력해주세요.').removeClass('is-safe').addClass('is-danger')
    $('#input-username').focus()
    return
  }
  if (!is_nickname(username)) {
    $('#help-id').text('⚠ 아이디의 형식을 확인해주세요. 영문과 숫자, 일부 특수문자(._-) 사용 가능. 2-10자 길이').removeClass('is-safe').addClass('is-danger')
    $('#input-username').focus()
    return
  }
  $('#help-id').addClass('is-loading')
  $.ajax({
    type: 'POST',
    url: '/register/check_dup',
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
  let pw2 = $('#userPw2').val()

  if (pw == '' && pw2 == '') {
    $('#help-pw, #help-pw2').text('비밀번호를 입력해주세요.').removeClass('is-safe').addClass('is-danger')
    $('#input-pw').focus()
    return
  } else if (pw != pw2) {
    $('#help-pw, #help-pw2').text('비밀번호가 일치하지 않습니다.').removeClass('is-safe').addClass('is-danger')
    $('#input-pw').focus()
    return
  } else {
    $('#help-pw').text('비밀번호가 일치합니다.').removeClass('is-danger').addClass('is-success')
    $('#help-pw2').text('✅').removeClass('is-danger').addClass('is-success')
  }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////

// 회원가입
function register() {
  let username = $('#userid').val()
  let nickname = $('#userNick').val()
  let pw = $('#userPw').val()
  let pw2 = $('#userPw2').val()

  // 01. 아이디
  if ($('#help-id').hasClass('is-danger')) {
    alert('아이디를 다시 확인해주세요.')
    return
  } else if (!$('#help-id').hasClass('is-success')) {
    alert('아이디 중복확인을 해주세요.')
    return
  }

  // 02. 비번
  if (pw == '' && pw2 == '') {
    $('#help-pw, #help-pw2').text('비밀번호를 입력해주세요.').removeClass('is-safe').addClass('is-danger')
    $('#input-pw').focus()
    return
  } else if (pw != pw2) {
    $('#help-pw, #help-pw2').text('비밀번호가 일치하지 않습니다.').removeClass('is-safe').addClass('is-danger')
    $('#input-pw').focus()
    return
  } else {
    $('#help-pw').text('비밀번호가 일치합니다.').removeClass('is-danger').addClass('is-success')
    $('#help-pw2').text('✅').removeClass('is-danger').addClass('is-success')
  }

  Swal.fire({
    icon: 'success',
    title: '환영해요!!',
    text: '회원가입이 완료되었어요!',
    confirmButtonColor: '#075da5',
  })

  $.ajax({
    type: 'POST',
    url: '/register/save',
    data: {
      id_give: username,
      nickname_give: nickname,
      pw_give: pw,
      pw2_give: pw2,
    },
    success: function (response) {
      if (response['result'] == 'success') {
        Swal.fire({
          icon: 'success',
          title: '환영해요!!',
          text: '회원가입이 완료되었어요!',
          showConfirmButton: false,
        })
        setTimeout(function go_login() {
          window.location.href = '/login'
        }, 700)
      }
    },
  })
}
