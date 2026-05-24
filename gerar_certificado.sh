#!/bin/bash
# gerar_certificado.sh
# Gera certificado SSL auto-assinado para uso local/demonstração

echo "🔐 Gerando certificado SSL auto-assinado..."

mkdir -p certs

openssl req -x509 \
  -newkey rsa:2048 \
  -keyout certs/key.pem \
  -out certs/cert.pem \
  -days 365 \
  -nodes \
  -subj "/C=BR/ST=SP/L=SaoPaulo/O=FIAP/OU=Totem/CN=localhost"

echo ""
echo "✅ Certificado gerado com sucesso em certs/"
echo "   cert.pem → certificado público"
echo "   key.pem  → chave privada"
echo ""
echo "⚠️  Como é auto-assinado, o navegador vai exibir aviso de segurança."
echo "   Clique em 'Avançado' → 'Prosseguir para localhost' para continuar."
