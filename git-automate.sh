#!/bin/bash

# Verifica se uma mensagem de commit foi fornecida
if [ -z "$1" ]; then
    echo "Erro: Você precisa fornecer uma mensagem para o commit."
    echo "Uso: ./git-automate.sh 'Sua mensagem de commit aqui'"
    exit 1
fi

# Mensagem do commit (passada como argumento)
COMMIT_MESSAGE="$1"

# Nome da branch atual
CURRENT_BRANCH=$(git branch --show-current)

# Verifica se há alterações para commitar
if [[ -n $(git status -s) ]]; then
    echo "Fazendo commit das alterações..."
    git add .
    git commit -m "$COMMIT_MESSAGE"
    git push origin "$CURRENT_BRANCH"
else
    echo "Nenhuma alteração para commitar."
fi

# Faz o merge na branch main
echo "Mudando para a branch main..."
git checkout main

echo "Atualizando a branch main..."
git pull origin main

echo "Fazendo merge da branch $CURRENT_BRANCH na main..."
git merge "$CURRENT_BRANCH"

echo "Enviando alterações para o repositório remoto..."
git push origin main

echo "Voltando para a branch $CURRENT_BRANCH..."
git checkout "$CURRENT_BRANCH"

echo "Processo concluído!"