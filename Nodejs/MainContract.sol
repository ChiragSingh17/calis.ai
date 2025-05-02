//SPDX-License-Indetifier: MLT

pragma solidity 0.8.24;
import "@openzeppelin/contract/ERC20/IERc20";
contract Maincontract is IERc20{
    string private _name;
    string private _symbol;
    string private _decimal;
    string private _totalSupply;

    mapping(address -> uint256) private _balances;
    event Transfer(address to , address from , uint256 amount);
    contstructor(string memory tokenname,string memory tokensymbol){
        _name = tokenname;
        _symbol = tokensymbol;
        _decimal = 18;

    }
    function balanceOf(address account) public view return(uint256){
        return _balances(account);

    }
    function transfer(address to , uint256 amount ) public returns(bool){
        address owner = msg.sender;
        if(owner == address(0)){
            revert("Invalid sender");
        }
    
    uint256 frombalance = _balances(from);
    if(frombalance = 0){
        revert("cannot sendzero tokens");
    }
    _balances[msg.sender]=frombalance -amount;
    _balances[to] +=amount;

    }
}