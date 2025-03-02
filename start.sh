#!/bin/bash
echo ">>> Avvio servizio Cartomante AI con waitress..."
waitress-serve --port=$PORT app:app
