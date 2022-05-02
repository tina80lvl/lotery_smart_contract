const Lotery = artifacts.require("Lotery")

contract("Lotery", (accounts) => {
    before(async () => {
        instance = await Lotery.deployed()
    })

    it("zero start balance", async () => {
        let balance = await instance.getBalance();
        assert.equal(balance, 0, 'should be 0');
    })

    it("balance increase", async () => {
        let val = web3.utils.toWei('3', 'ether');
        await instance.enter({from: accounts[1], value: val});

        let balance = await instance.getBalance();
        assert.equal(balance, val, 'should be 3eth in wei');

        let addresses = await instance.getParticipants();
        assert.equal(addresses.length, 1, 'should be empty');
    })

    it("lonley partisipant won", async () => {
        let addresses = await instance.getParticipants();
        assert.equal(addresses.length, 1, 'should be 1');

        let winnerAddress = await instance.pickRandomWinner.call({from: accounts[0], value: 0});
        assert.equal(winnerAddress, addresses[0], 'should be equal');
    })

    it("clear partisipant list and balance", async () => {
        let addresses = await instance.getParticipants();
        assert.equal(addresses.length, 1, 'should be 1');

        await instance.pickRandomWinner({from: accounts[0], value: 0});

        let list = await instance.getParticipants();
        assert.equal(list.length, 0, 'should be 0');

        let balance = await instance.getBalance();
        assert.equal(balance, 0, 'should be 0');
    })

})