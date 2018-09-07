from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=app.config['DEBUG'],
        port=2000,
        # 开启多线程
        threaded=True,
        # 多线程是 processes
    )

"""
postman
https://wiki.archlinux.org/index.php/MySQL_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)
mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
mysqladmin --version
mysqladmin -u root password "[enter your password here]";
mysql -u root -p

systemctl start mariadb
"""
