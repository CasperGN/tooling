using System;
using System.Security.Cryptography;

namespace VNCHexDecoder
{
    class Program
    {
        public static byte[] ToByteArray(String HexString)
        {
            int NumberChars = HexString.Length;
            byte[] bytes = new byte[NumberChars / 2];

            for (int i = 0; i < NumberChars; i += 2)
            {
                bytes[i / 2] = Convert.ToByte(HexString.Substring(i, 2), 16);
            }

            return bytes;
        }

        static void Main(string[] args)
        {
            Console.WriteLine("Input Hex string:");
            
            string password = Console.ReadLine();
            byte[] key = { 23, 82, 107, 6, 35, 78, 88, 7 };
            byte[] passArr = ToByteArray(password);
            byte[] response = new byte[passArr.Length];

            // reverse the byte order
            byte[] newkey = new byte[8];
            for (int i = 0; i < 8; i++)
            {
                // revert key[i]:
                newkey[i] = (byte)(
                    ((key[i] & 0x01) << 7) |
                    ((key[i] & 0x02) << 5) |
                    ((key[i] & 0x04) << 3) |
                    ((key[i] & 0x08) << 1) |
                    ((key[i] & 0x10) >> 1) |
                    ((key[i] & 0x20) >> 3) |
                    ((key[i] & 0x40) >> 5) |
                    ((key[i] & 0x80) >> 7)
                    );
            }
            key = newkey;
            // reverse the byte order

            DES des = new DESCryptoServiceProvider();
            des.Padding = PaddingMode.None;
            des.Mode = CipherMode.ECB;

            ICryptoTransform dec = des.CreateDecryptor(key, null);
            dec.TransformBlock(passArr, 0, passArr.Length, response, 0);

            Console.WriteLine(System.Text.ASCIIEncoding.ASCII.GetString(response));
            Console.WriteLine("Hit enter to close...");
            Console.ReadLine();
        }
    }
}
