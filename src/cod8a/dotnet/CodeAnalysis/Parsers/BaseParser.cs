using CodeAnalyzer.models;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using System;
using System.Collections.Generic;
using System.Text;

namespace CodeAnalyzer.Parsers
{
    public abstract class BaseParser<T>
    {
        /// <summary>
        /// Gets the name of the file associated with this instance.
        /// </summary>
        public abstract string Name { get; init; }
        public abstract T Parse();
    }
}
