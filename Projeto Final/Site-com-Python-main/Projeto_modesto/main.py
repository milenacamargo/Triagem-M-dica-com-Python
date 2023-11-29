from website import create_app

app = create_app()
#rodar o servidor web
if __name__ == '__main__':
  app.run(debug=True)
