import sys
from pyRSC import RSC, Assembler

def main():
    args = sys.argv[1:]
    if args:
        match args[0]:
            case "assembler":
                asm = Assembler(args[1])
                asm.logisim_format(args[2])
            case "run":
                pyRSC = RSC(args[1])
                pyRSC.run()
            case "debug":
                pyRSC = RSC(args[1], debug=True)
                pyRSC.run()
            case "help":
                print("usage: pyRSC [run|assembler] [in] [out]\nThe assembler is used for producing logisim-formatted binaries of your microcode.\nThe run command is to emulate your given microcode file, output is not needed.")
            case _:
                print("usage: pyRSC [run|assembler] [in] [out]")
    else:
        print("usage: pyRSC [run|assembler] [in] [out]\nThe assembler is used for producing just logisim input.\nThe run command is to emulate your given microcode file, output is not needed.")

if __name__ == "__main__":
    main()