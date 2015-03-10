alias ls="ls -hG"
alias l="ls -Al"
alias ll="ls -al"
alias ..="cd .."
alias edit="open -a \"Sublime Text.app\""
alias ip="ifconfig | grep \"192.168\""

export PS1="\w > "

[[ -r ~/.profile_local ]] && . ~/.profile_local