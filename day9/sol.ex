
defmodule Sol do
  @type id::integer()
  @type length::integer()
  @type file::{id(), length()}
  @type space::{length()}
  @type token::file()|space()

  def part1 do
    digits = parseInput()
    blockMap = getBlockMap(digits, 0, 0, [])
    revBlockMap = Enum.reverse(blockMap)
    fileCount = Enum.count(blockMap, fn e-> e >= 0 end)
    {ind, sum}=Enum.reduce(blockMap, {0,0}, fn e, {i,sum} ->
      if (e < 0) do {i, sum} else {i + 1, sum + (i*e)} end
    end)
    fragMap=fragmenter(blockMap, revBlockMap, [], 0, fileCount)
    {fragMap,fragSum(fragMap,0, 0), sum}
  end

  def example do
    ex = "2333133121
    414131  4 02"
    digits = parse(ex)
    blockMap = getBlockMap(digits, 0,0, [])
    revBlockMap = Enum.reverse(blockMap)
    fileCount = Enum.count(blockMap, fn e-> e >= 0 end)
    fragMap=fragmenter(blockMap, revBlockMap, [], 0, fileCount)
    {fragMap,fragSum(fragMap,0, 0)}
  end

  def fragSum([],_,sum) do sum end
  def fragSum([curr|fragMap], index, sum) do
    fragSum(fragMap, index + 1, sum + (curr*index))
  end

  def fragmenter(_,_,fragMap, fragLen, fileCount) when fragLen >= fileCount do Enum.reverse(fragMap) end
  def fragmenter(map=[c0|rest0], rev=[c1|rest1], fragMap, fragLen, fileCount) when c0 !== -1 do
    fragmenter(rest0, rev, [c0|fragMap], fragLen + 1, fileCount)
  end
  def fragmenter(map=[-1|rest0], rev=[-1|rest1], fragMap, fragLen, fileCount) do
    fragmenter(map, rest1, fragMap, fragLen, fileCount)
  end
  def fragmenter(map=[-1|rest0], rev=[c1|rest1], fragMap, fragLen, fileCount) when c1 !== -1 do
    fragmenter(rest0, rest1, [c1|fragMap], fragLen + 1, fileCount)
  end




  def getBlockMap([], _,_, blockMap) do Enum.reverse(blockMap) end
  def getBlockMap([digit|digits], index, idcnt, blockMap) when rem(index, 2) !== 0 do
    block = Enum.map(1..digit, fn _-> -1 end)
    getBlockMap(digits, index + 1, idcnt, block++blockMap)
  end
  def getBlockMap([digit|digits], index,idcnt, blockMap) do
    block = Enum.map(1..digit, fn _-> idcnt end)
    getBlockMap(digits, index + 1, idcnt + 1, block++blockMap)
  end

  def parseInput do
    fPath="input.txt"
    {:ok, data} = File.read(fPath)
    parse(data)
  end

  def parse(data) do
    data=String.replace(data, ~r/\s+/, "")
    digits = collectDigits(data, [])
  end

  def collectDigits(<<>>, digits) do Enum.reverse(digits) end
  def collectDigits(<<curr, rest::binary>>, digits) do collectDigits(rest, [curr - ?0|digits]) end
end
