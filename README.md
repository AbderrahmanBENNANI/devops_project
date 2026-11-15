# LocalFirst CV Platform

MVP d'une application Local-First de création de CV et lettres, avec API Python/Flask,
génération PDF, frontend web stockant les brouillons dans IndexedDB, Docker Compose,
Cloudflare Tunnel et supervision Prometheus/Grafana.

## Prérequis
- Docker Desktop (Windows/macOS) ou Docker Engine + Compose (Linux)
- Git
- Un compte Cloudflare et un domaine pour l'accès public (facultatif en local)
- Un compte Stripe uniquement pour activer les paiements

## Démarrage local
1. Copier `.env.example` vers `.env`.
2. Remplacer `APP_SECRET_KEY` par une valeur aléatoire forte.
3. Lancer : `docker compose up --build -d`
4. Ouvrir `http://localhost:8080`
5. Vérifier `http://localhost:5000/health` et `http://localhost:9090` (Prometheus).
6. Grafana : `http://localhost:3000` (identifiants définis dans `.env`).

## Cloudflare Tunnel
Le service cloudflared est désactivé par défaut dans le profil `cloudflare`.
Créer un tunnel dans Cloudflare Zero Trust, récupérer le token, le placer dans
`CLOUDFLARE_TUNNEL_TOKEN`, puis lancer :
`docker compose --profile cloudflare up -d`

Dans Cloudflare, router `api.tondomaine.tld` vers `http://api:5000` et
`app.tondomaine.tld` vers `http://web:8080`. Ne jamais exposer directement les ports
de l'API, Prometheus ou Grafana sur Internet.

## Structure
- `backend/` API, validation, PDF, tests
- `frontend/` interface PWA et stockage IndexedDB
- `infra/` Prometheus et Grafana
- `.github/workflows/` tests et scan Trivy

## Limites de ce MVP
- Paiement Stripe : variables et webhook à configurer avant activation.
- Le frontend conserve les brouillons dans le navigateur. Le serveur ne persiste pas les CV.
- Avant une mise en production : ajouter une politique de confidentialité, conditions
  d'utilisation, sauvegarde de configuration, tests de charge, audit de sécurité,
  gestion des secrets et validation juridique des paiements.
- Ne pas considérer le filigrane comme une protection anti-copie absolue.
