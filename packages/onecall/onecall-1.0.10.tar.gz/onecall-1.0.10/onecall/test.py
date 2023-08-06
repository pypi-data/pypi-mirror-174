from phemex import Phemex


def main():
    client = Phemex(key="2f5efa34-59e8-4eb8-95f1-821d72054fe9",
                         secret="WcrWD3PceZ4KaeiMx1_z0ecQZJ7-Yq7CUbeNGaX7SrJjOGIyYzk0Yi03YzUyLTRlYmEtYWJiZi00Y2RjZjMxMzk0MDQ",
                         debug=True)

    print(client.get_balance('BTC'))


if __name__ == "__main__":
    main()
