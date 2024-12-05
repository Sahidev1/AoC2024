
# if input string consists of m characters then this solution has a worst case complexity of O(m * logm)
defmodule Sol do
  @type movement :: nil|:vertical | :horizontal | :diagdown | :diagup

  def main do
    data = parseInput()
    proc(data, 0, 0, 0)
  end

  def example do
    examplestr = "MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"

    data = parse(examplestr)
    proc(data, 0, 0, 0)
  end

  def proc(data, row, col, count) do
    curr = matrixGetChar(data, row, col)
    cnt = count
    cnt = cond do
      curr === 'X' ->
        cnt + searchFrom(data, row, col, 'XMAS', nil)
      curr === 'S' ->
        cnt + searchFrom(data, row, col, 'SAMX', nil)
      true -> cnt
    end

    [row, col] = if (col < data[:cols]) do
      [row, col + 1]
    else
      [row + 1, 0]
    end

    if (row < data[:rows]) do
      proc(data, row , col, cnt)
    else
      cnt
    end
  end

  def searchFrom(data, row, col, pattern, nil) do
    [curr | rest] = pattern
    availRows = data[:rows] - row - 1
    availCols = data[:cols] - col - 1
    v = if(availCols >= 3) do searchFrom(data, row, col + 1, rest, :horizontal)  else 0 end
    v = if(availRows >= 3) do v + searchFrom(data, row + 1, col, rest, :vertical) else v end
    v = if(availRows >= 3 && availCols >= 3) do v + searchFrom(data, row+1, col+1, rest, :diagdown) else v end
    v = if(availCols >= 3 && row >= 3) do v + searchFrom(data, row - 1, col + 1, rest, :diagup) else v end
  end
  def searchFrom(data, row, col, [], d) do 1 end
  def searchFrom(data, row, col, pattern, d) do
    [curr | rest] = pattern
    currVal = matrixGetChar(data, row, col)
    if ([curr] !== currVal) do
      0
    else
      [row, col] = matrixMv([row, col], d)
      searchFrom(data, row, col, rest, d)
    end
  end

  def matrixMv([row, col], :horizontal) do [row, col + 1 ] end
  def matrixMv([row, col], :vertical) do [row + 1, col] end
  def matrixMv([row, col], :diagdown) do [row + 1, col + 1] end
  def matrixMv([row, col], :diagup) do [row - 1, col + 1] end


  def matrixGetChar(data,row, col) do
    rowdata = Map.get(data[:matrix], row)
    char = Map.get(rowdata, col)
    [char]
  end

  def parseInput do
    fPath = "input.txt"
    {:ok, data} = File.read(fPath)
    parse(data)
  end
  def parse(str) do

    data = String.split(str, "\n", trim: true)

    {_,data} = Enum.reduce(data, {0,%{}}, fn cl, acc->
      {i,map} = acc
      list = to_charlist(cl)
      {_,list} = Enum.reduce(list,{0,%{}} ,fn e,acc->
        {i, map} = acc
        map=Map.put(map, i, e)
        i = i + 1
        {i,map}
      end)

      map=Map.put(map, i, list)
      i = i + 1
      {i, map}
    end)
    [rows: map_size(data), cols: Map.get(data,0)|>map_size()  ,matrix: data]
  end
end
