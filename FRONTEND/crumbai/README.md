# CrumbAI - NextJS Frontend

## Getting Started

Follow these instructions to set up the project locally for development and testing purposes.

### Prerequisites

You will need the following installed on your system:
- git
- Node.js (LTS version)
- npm

### Installation

- Clone the project repository:

```bash
git clone https://github.com/HamzDevelopment/CrumbAI
```

- Navigate to the directory:

```bash
cd CrumbAI/FRONTEND/crumbai
```

- Install the dependencies:

```bash
npm install
```

- Edit the `.env` file with your database info and keys

- Run the following command to generate the database tables using prisma:

```bash
npx prisma migrate dev
```

- Run the server:

```bash
npm run dev
```

## Built With

- [Next.js](https://nextjs.org/) - The React framework used for server-side rendering and static site generation.
- [ShadCN UI](https://ui.shadcn.com/) - For building high-quality, accessible design system components.
- [TypeScript](https://www.typescriptlang.org/) - For type-safe code.
