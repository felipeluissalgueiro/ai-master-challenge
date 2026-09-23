'use client';

export default function GlobalError({reset}: {error: Error & {digest?: string}; reset: () => void}) {
  return (
    <html lang="pt-BR">
      <body>
        <div className="fatal-state">
          <h1>O shell não pôde ser carregado</h1>
          <p>Nenhum dado foi substituído por zero. Tente carregar a aplicação novamente.</p>
          <button type="button" onClick={reset}>Tentar novamente</button>
        </div>
      </body>
    </html>
  );
}
