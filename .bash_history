sudo apt-get update
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wg
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev git python-pip sqlite3
mkdir codeit-django
cd codeit-django
code .
curl https://pyenv.run | bash
echo $SHELL
sed -Ei -e '/^([^#]|$)/ {a \
export PYENV_ROOT="$HOME/.pyenv"
a \
export PATH="$PYENV_ROOT/bin:$PATH"
a \
' -e ':a' -e '$!{n;ba};}' ~/.profile
echo 'eval "$(pyenv init --path)"' >>~/.profile
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zprofile
pyenv --version
pyenv versions
pyenv install 3.7.13
pyenv install 3.8.13
pyenv versions
pyenv virtualenv 3.7.13 django-envs
pyenv versions
pyenv global 3.8.13
pyenv versions
cd codeit-django
pyenv versions
pyenv local django-envs
pip3 install django==2.2
django-admin --version
pip3 list
echo $SHELL
sudo apt-get install zsh
chsh -s `which zsh`
echo $SHELL.
echo $SHELL
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
