from robobrowser import RoboBrowser
from BeautifulSoup import BeautifulSoup


def CreateAccount():
    username = "John"
    email = "JohnD@outlook.com"
    password = "John123"
    password_re = "John123"
    fname = "John"
    lname = "Doe"

    browser = RoboBrowser(parser='html.parser')
    login_url = 'http://artificialeducation.com/create-account-page/'
    browser.open(login_url)
    form = browser.get_form(id='swpm-registration-form')
    form['user_name'].value = username
    form['email'].value = email
    form['password'].value = password
    form['password_re'].value = password_re
    form['first_name'].value = fname
    form['last_name'].value = lname
    browser.submit_form(form)
    browser.open('http://artificialeducation.com/login-success-page/')
    print(browser.parsed)




def Login():
    username = 'Betty123'
    password = 'Betty123'

    browser = RoboBrowser(parser='html.parser')
    login_url = 'http://artificialeducation.com/login/'
    browser.open(login_url)
    form = browser.get_form(id='swpm-login-form')
    form['swpm_user_name'].value = username
    form['swpm_password'].value = password
    browser.submit_form(form)
    browser.open('http://artificialeducation.com/login-success-page/')


    soup = BeautifulSoup(str(browser.parsed))

    success_message = soup.findAll('p')
    final_message = ''

    for node in success_message:
        final_message += ''.join(node.findAll(text=True))

    print(final_message)
    if 'Login succeed' in final_message:
        print('Will pass to Main_Storyboard')
    else:
        print('Login/Account Creation failed')

Login()