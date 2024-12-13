
# if input string consists of m characters then this solution has a worst case complexity of O(m * logm)
defmodule Sol do
  @type movement :: nil|:vertical | :horizontal | :diagdown | :diagup

  def part1 do
    data = parseInput()
    proc1(data, 0, 0, 0)
  end

  def part2 do
    data = parseInput()
    proc2(data, 0, 0)
  end

  def example2 do
    ex =
   "SSM
    MAT
    SAM"
    IO.puts(ex)
    data = parse(ex)
    proc2(data,0,0)
  end

  def example3 do
    ex =
   "MAS
    MAT
    MMS"
    IO.puts(ex)
    data = parse(ex)
    proc2(data,0,0)
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
    IO.puts(examplestr)
    {proc1(data, 0, 0, 0), proc2(data, 0, 0)}
  end

  def proc2([rows: r, cols: c, matrix: m], row, col) when row > r - 3 do 0 end
  def proc2(d=[rows: r, cols: c, matrix: m], row, col) when col > c - 3 do
    proc2(d, row + 1, 0)
  end
  def proc2(d, row, col) do
    val = if(is_xmas?(d,row,col)) do
      1
    else
      0
    end
    val + proc2(d, row, col + 1)
  end

  def is_xmas?(d, i , j) do
    case matrixGetChar(d, i + 1, j + 1) do
      'A'->
        top = [matrixGetChar(d, i, j), matrixGetChar(d, i, j + 2)]
        bottom = [matrixGetChar(d, i + 2, j), matrixGetChar(d, i + 2, j + 2)]
        mapping = mapTop(top)
        case mapping do
          nil -> false
          _-> bottom === mapping
        end
      _->false
    end
  end

  def mapTop(['M','M']) do ['S', 'S'] end
  def mapTop(['S','S']) do ['M','M'] end
  def mapTop(['S','M']) do ['S','M'] end
  def mapTop(['M','S']) do ['M','S'] end
  def mapTop(_) do nil end




  def proc1(data, row, col, count) do
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
      proc1(data, row , col, cnt)
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
