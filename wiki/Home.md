# Django Production Boilerplate Wiki

This wiki explains how to run, extend, and operate the boilerplate.
It serves developers learning production Django and experienced teams evaluating its infrastructure decisions.

## Start Here

New to Django or this repository:

1. Follow the [Quick Start](Quick-Start).
2. Build one complete feature with [Extending the Boilerplate](Extending-the-Boilerplate).
3. Learn how [Email](Email) and [Caching](Cache) are selected through environment configuration.
4. Read [Deployment](Deployment) before exposing the application publicly.

Already comfortable with Django:

1. Review [Architecture](Architecture) for boundaries and deliberate omissions.
2. Check [Deployment](Deployment) for container and native-host topology.
3. Review [Cache](Cache) and [Email](Email) for backend contracts and failure behavior.
4. Use the [Roadmap](Roadmap) to decide what belongs in the boilerplate versus an application.

## Core Principle

The boilerplate owns infrastructure defaults, not product architecture.
Django's native interfaces remain the boundary for storage, cache, email, authentication, and application modules wherever practical.

This keeps local and production providers replaceable without spreading environment checks through feature code.

## Documentation Map

| Goal | Page |
| --- | --- |
| Run Django locally | [Quick Start](Quick-Start) |
| Understand project boundaries | [Architecture](Architecture) |
| Add a complete module | [Extending the Boilerplate](Extending-the-Boilerplate) |
| Configure caching or Redis | [Cache](Cache) |
| Configure Mailpit or SMTP | [Email](Email) |
| Deploy and operate the application | [Deployment](Deployment) |
| Review planned additions | [Roadmap](Roadmap) |
| Review current release changes | [Release Notes](Release-Notes) |

## Source of Truth

Wiki pages are published from Markdown in the repository after changes reach `main`.
Contribute documentation through normal pull requests so documentation changes receive the same review as code.
